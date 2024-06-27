from loguru import logger
from configs import BaseConfig
import ftplib
import os


class FtpUtil:
    def __init__(
        self,
        host=BaseConfig.FTP_HOST,
        user=BaseConfig.FTP_USER,
        password=BaseConfig.FTP_PASSWORD,
        post=21,
        encoding="utf-8",
        pasv=BaseConfig.FTP_PASSIVE,
    ):
        self.ftp = ftplib.FTP(host, user, password, encoding=encoding)  # 连接ftp服务器
        self.ftp.set_pasv(pasv)  # 设置被动模式

    def close(self):
        self.ftp.quit()  # 关闭服务器

    # 上传文件
    def uploadfile(self, localfile, remotefile):
        """上传文件

        Args:
            localfile (_type_): 本地文件
            remotefile (_type_): 远程文件
        """
        if not os.path.isfile(localfile):
            logger.info(f"{localfile} 不是文件!")
        # filename = os.path.split(localfile)[-1]  # 获取文件名
        remotepath, remotefile_name = os.path.split(remotefile)        
        self.ftp.cwd(remotepath)
        with open(localfile, "rb") as file:  # 读取文件
            self.ftp.storbinary(f"STOR {remotefile_name}", file)  # 二进制存储

    # 上传文件夹
    def uploaddir(self, localdir, remotepath):
        """上传文件夹

        Args:
            localdir (_type_): 本地文件夹
            remotepath (_type_): 远程路径
        """
        if not os.path.isdir(localdir):
            logger.info(f"{localdir} 不是文件夹")
        dirname = os.path.split(localdir)[-1]  # 文件夹名称
        new_remotepath = remotepath + dirname + "/"  # os.path.join(remotepath, dirname)
        self.makedir(dirname, remotepath)
        for localfile in os.listdir(localdir):
            src = os.path.join(localdir, localfile)
            if os.path.isfile(src):
                self.uploadfile(src, new_remotepath)
            elif os.path.isdir(src):
                self.uploaddir(src, new_remotepath)  # 嵌套的文件夹：{src}
        self.ftp.cwd("..")

    # 创建文件夹
    def makedir(self, dirname, remotepath, new_remotepath):
        try:
            self.ftp.cwd(new_remotepath)
            logger.info(f"{new_remotepath} 文件夹已存在")
        except ftplib.error_perm:
            try:
                self.ftp.cwd(remotepath)
                self.ftp.mkd(dirname)
                logger.info(f"文件夹创建成功：{remotepath}{dirname}")
            except ftplib.error_perm as ex:
                logger.info(f"创建文件夹失败：{ex}")

    # 下载文件
    def downloadfile(self, localfile, remotefile):
        remotepath, remotefile_name = os.path.split(remotefile)
        if self.is_exist(remotepath, remotefile_name):  # 判断文件是否存在
            with open(localfile, "wb") as file:
                self.ftp.retrbinary(f"RETR {remotefile}", file.write)
            logger.info(f"文件下载成功：{localfile}")
            return True
        else:
            logger.info(f"文件不存在: {localfile}")
            return False

    # 下载文件夹
    def downloaddir(self, localdir, remotepath):
        if not self.is_exist(remotepath):
            logger.info(f"远程文件夹不存在: {remotepath}")
            return False
        else:
            if not os.path.exists(localdir):
                logger.info(f"创建本地文件夹：{localdir}")
                os.makedirs(localdir)
            self.ftp.cwd(remotepath)
            remotenames = self.ftp.nlst()
            for file in remotenames:
                localfile = os.path.join(localdir, file)
                if file.find(".") == -1:
                    if not os.path.exists(localfile):  # 递归文件夹：{remotepath}
                        os.makedirs(localfile)
                    self.downloaddir(localfile, file)
                else:
                    self.downloadfile(localfile, file)
            self.ftp.cwd("..")
            return True

    # 判断文件/文件夹是否存在
    def is_exist(self, remotepath, filename=None):
        try:
            self.ftp.cwd(remotepath)
        except ftplib.error_perm:
            logger.info(f"远程路径不存在: {remotepath}")
            return False
        if filename is not None:
            filelist = self.ftp.nlst()
            if filename in filelist:
                logger.info(f"存在该文件{filename}")
                return True
            else:
                logger.info(f"没有该文件{filename}")
        else:
            logger.info(f"远程路径存在{remotepath}")
            return True
    
    # 删除文件
    def deletfile(self, remotefile):
        remotepath, remotefile_name = os.path.split(remotefile)
        if self.is_exist(remotepath, remotefile_name):
            self.ftp.delete(remotefile_name)
            logger.info(f"远程文件已删除: {remotefile_name}")
            return True
        else:
            logger.info(f"远程文件不存在: {remotefile_name}")
            return False

    # 删除文件
    def deletfile(self, filename, remotepath):
        if self.is_exist(remotepath, filename):
            self.ftp.delete(filename)
            logger.info(f"远程文件已删除: {filename}")
            return True
        else:
            logger.info(f"远程文件不存在: {filename}")
            return False
    

    # 删除文件夹
    def deletedir(self, remotepath):
        if self.is_exist(remotepath):
            filelist = self.ftp.nlst()
            if len(filelist) != 0:
                for file in filelist:
                    new_remotepath = os.path.join(remotepath, file).replace("\\", "/")
                    if file.find(".") == -1:
                        self.deletedir(new_remotepath)
                    else:
                        self.deletfile(file, remotepath)
            self.ftp.rmd(remotepath)
            logger.info(f"远程文件夹删除成功: {remotepath}")
            return True
        else:
            logger.info(f"远程文件夹不存在: {remotepath}")
            return False
