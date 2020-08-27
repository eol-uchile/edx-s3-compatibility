from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.base import ContentFile

class S3Boto3StorageWrapper(S3Boto3Storage):
    def __force_byte_content(self, content):
        block = content.read(1024)
        content.seek(0)

        if not isinstance(block, bytes):
            return ContentFile(content.read().encode())
        return content

    def save(self, name, content, max_length=None):
        content = self.__force_byte_content(content)
        return super().save(name, content, max_length)

    
class ImportExportS3Boto3Storage(S3Boto3Storage):
    def save(self, name, content, max_length=None):
        if name.endswith("tar.gz"):
            content.content_type = 'Application/Gzip'
        return super().save(name, content, max_length)
