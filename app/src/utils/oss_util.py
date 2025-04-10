import oss2
import os

def upload_to_oss(local_file_path, bucket_name, access_key_id, access_key_secret, endpoint):
    # 创建 Bucket 实例
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    
    # 获取文件名
    file_name = os.path.basename(local_file_path)
    
    try:
        # 上传文件
        bucket.put_object_from_file(file_name, local_file_path)
        
        # 生成公网访问链接（默认有效期1小时）
        url = bucket.sign_url('GET', file_name, 3600)
        
        # 如果你的 Bucket 是公共读取权限，也可以直接使用这种方式构造 URL
        # url = f"https://{bucket_name}.{endpoint}/{file_name}"
        
        return {
            'status': 'success',
            'url': url,
            'message': '文件上传成功'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'上传失败：{str(e)}'
        }

# 使用示例
if __name__ == '__main__':
    
    ACCESS_KEY_ID = ''
    ACCESS_KEY_SECRET = ''
    BUCKET_NAME = 'my-bucket-van'
    ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'  # 例如：'oss-cn-beijing.aliyuncs.com'
    
    # 本地图片路径
    local_image_path = 'app/src/source/卡通少女.png'
    
    # 上传图片
    result = upload_to_oss(
        local_image_path,
        BUCKET_NAME,
        ACCESS_KEY_ID,
        ACCESS_KEY_SECRET,
        ENDPOINT
    )
    
    print(result)
    
  