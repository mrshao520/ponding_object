from sqlalchemy import insert, create_engine, String, INT, DateTime, text, bindparam, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from loguru import logger
from datetime import datetime


class Base(DeclarativeBase):
    pass

class PondingTable(Base):
    __tablename__ = 'ponding_table'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    time: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64), nullable=False)
    position: Mapped[str] = mapped_column(String(128), nullable=False)
    lati_longi_tude: Mapped[str] = mapped_column(String(64))
    depth_value: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(256))
    
    def __repr__(self) -> str:
        return f"PondingTable(id={self.id!r}, date={self.date!r}, time={self.time!r} \
, city={self.city!r}, position={self.position!r} \
, lati_longi_tude={self.lati_longi_tude!r} \
, depth_value={self.depth_value!r} \
, description={self.description!r})"

class SummaryTable(Base):
    __tablename__ = 'summary_table'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=False)
    volume: Mapped[int] = mapped_column(INT, nullable=False)
    
    def __repr__(self) -> str:
        return f"SummaryTable(id={self.id!r}, city={self.city!r} \
, description={self.description!r}, volume={self.volume!r})"

class Base_():
    engine = create_engine("mysql+pymysql://root:123456@mysql/water_database",
                            echo=True)
    Session = sessionmaker(engine)

class OperatePonding(Base_):
    def __init__(self) -> None:
        pass
    
    def query_summary_data(self):
        ret = {}
        with self.Session() as session:
            results = session.query(SummaryTable).order_by(SummaryTable.city, SummaryTable.description).all()
            for res in results:
                if res.city in ret:
                    ret[res.city][res.description] = res.volume
                else:
                    ret[res.city] = {res.description:res.volume}
                logger.info(res)
        return ret
    
    def delete_ponding_data(self, content:list):
         with self.engine.connect() as conn:
            res = conn.execute(text('DELETE FROM ponding_table WHERE id = :id '),
                         content)
            conn.commit()
    
    # 根据城市，开始时间，结束时间 查询数据库
    def query_ponding_data(self, city, startTime, endTime):
        ret = []
        with self.Session() as session:
            results = session.query(PondingTable).filter(PondingTable.city == city, 
                                               PondingTable.date > startTime, 
                                               PondingTable.date < endTime).order_by(PondingTable.date.desc()).all()
            for res in results:
                tmp = {}
                tmp['id'] = res.id
                tmp['日期'] = res.date.strftime('%Y-%m-%d %H:%M:%S')
                tmp['时间'] = res.time
                tmp['城市'] = res.city
                tmp['地点'] = res.position
                tmp['经纬度'] = res.lati_longi_tude
                tmp['深度值'] = res.depth_value
                tmp['描述'] = res.description
                ret.append(tmp)
                logger.info(res)
        return ret
    
    # 插入数据库，在插入的时候根据日期，城市，地点去重
    def insert_ponding_data_dedup(self, results:list):
        with self.engine.connect() as conn:
            res = conn.execute(text('''INSERT INTO ponding_table \
(date, time, city, position, lati_longi_tude, depth_value, description) \
SELECT :日期, :时间, :城市, :地点, :经纬度, :深度值, :描述 \
FROM DUAL WHERE NOT EXISTS  \
(SELECT city FROM ponding_table WHERE \
date=:日期 and city=:城市 and position=:地点) '''),
                         results)
            conn.commit()
    
    # 插入数据库   
    def insert_ponding_data(self, results:list):
        with self.Session() as session:
            result = session.execute(
                insert(PondingTable).values(
                    # PondingTable.date = bindparam('日期'),
                    # PondingTable.time == bindparam('时间'),
                    # PondingTable.city == bindparam('城市'),
                    # PondingTable.position == bindparam('地点'),
                    # PondingTable.lati_longi_tude == bindparam('经纬度'),
                    # PondingTable.depth_value == bindparam('深度值'),
                    # PondingTable.description == bindparam('描述')
                    date = bindparam('日期'),
                    time = bindparam('时间'),
                    city = bindparam('城市'),
                    position = bindparam('地点'),
                    lati_longi_tude = bindparam('经纬度'),
                    depth_value = bindparam('深度值'),
                    description = bindparam('描述')
                    ), results
            )
            
            session.commit()
            
# if __name__ == '__main__':
#     res = [
#         {
#             "地点": "碑林:经九路化工南巷口",
#             "描述": "1",
#             "深度值": "1",
#             "日期": "2023-6-3 13:35",
#             "时间": "2023/6/3 13:35",
#             "城市": "西安",
#             "经纬度": "Error: ENGINE_RESPONSE_DATA_ERROR"
#         },
#         {
#             "地点": "天谷二路(云水一路到云水二路)",
#             "描述": "1",
#             "深度值": "1",
#             "日期": "2023-6-3 13:35",
#             "时间": "2023/6/3 13:35",
#             "城市": "西安",
#             "经纬度": "Error: ENGINE_RESPONSE_DATA_ERROR"
#         },
#         {
#             "地点": "省道107罗汉洞村口",
#             "描述": "1",
#             "深度值": "1",
#             "日期": "2023-6-3 13:35",
#             "时间": "2023/6/3 13:35",
#             "城市": "西安",
#             "经纬度": "Error: ENGINE_RESPONSE_DATA_ERROR"
#         }
#     ]
#     op = OperatePonding()
#     # op.insert_ponding_data(res)
#     results = op.query_ponding_data('西安', '2020-01-01 00:00:00', '2023-12-12 00:00:00')
#     for res in results:
#         logger.info(res)
    
    