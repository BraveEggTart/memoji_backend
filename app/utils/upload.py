import boto3
from uuid import uuid4

from app.config import settings

def upload_image_to_s3(file_name, bucket_name):

    object_name = f"{str(uuid4()).replace('-', '')}.{file_name.split('.')[-1]}"

    # 创建 S3 客户端，直接传入凭证
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        endpoint_url=settings.MINIO_URL,
    )

    # 上传文件
    s3_client.upload_file(file_name, bucket_name, object_name)
    print(f"上传成功: {file_name} 到 {bucket_name}/{object_name}")
    return object_name

# 使用示例
if __name__ == "__main__":
    upload_image_to_s3('sgtpng.png', 'memoji')
