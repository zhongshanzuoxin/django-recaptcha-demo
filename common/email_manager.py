
import boto3
import environ
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import logging

env = environ.Env()
logger = logging.getLogger(__name__)

def send_email(to, subject, body, source=None, html=False, attachments=None):
    """
    AWS SES を利用してメールを送信する関数。
    to          = 送り先アドレス (文字列またはリスト)
    subject     = 件名
    body        = メール本文
    source      = 送信元アドレス(From)
    html        = HTMLメールかどうか
    attachments = インライン添付ファイルリスト [{'mime_obj': MIMEオブジェクト, 'inline': True}, ...]
    """
    try:
        # 送信元が指定されていない場合はデフォルトを使用
        if not source:
            source = settings.MAIL_FROM
        
        # toが文字列の場合はリストに変換
        if isinstance(to, str):
            to_addresses = [to]
        else:
            to_addresses = to
        
        client = boto3.client(
            'ses',
            aws_access_key_id=env('MAIL_AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=env('MAIL_AWS_SECRET_ACCESS_KEY'),
            region_name="ap-northeast-1"
        )

        # 添付ファイルがない場合
        if not attachments:
            message_body = {}
            
            if html:
                message_body['Html'] = {
                    'Data': body,
                    'Charset': 'UTF-8'
                }
            else:
                message_body['Text'] = {
                    'Data': body,
                    'Charset': 'UTF-8'
                }
            
            response = client.send_email(
                Source=source,
                Destination={
                    'ToAddresses': to_addresses,
                },
                Message={
                    'Subject': {
                        'Data': subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': message_body
                }
            )
            logger.info(f"メール送信成功: {subject} to {to_addresses}")
            print(f"メール送信成功: MessageId={response['MessageId']}")
            return True

        # インライン添付ファイルがある場合のMIME構造作成
        msg_root = MIMEMultipart('mixed')
        msg_root['Subject'] = subject
        msg_root['From'] = source
        msg_root['To'] = ', '.join(to_addresses)
        msg_root['Date'] = email.utils.formatdate(localtime=True)

        # alternative パート（テキスト/HTML 切り替え用）
        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)

        # プレーンテキストパート（空でも必要）
        part_text = MIMEText('', 'plain', 'utf-8')
        msg_alternative.attach(part_text)

        # related パート（HTML + インライン画像）
        msg_related = MIMEMultipart('related')
        msg_alternative.attach(msg_related)

        # HTML本文
        part_html = MIMEText(body, 'html', 'utf-8')
        msg_related.attach(part_html)

        # インライン添付ファイルの処理
        for attach_dict in attachments:
            mime_obj = attach_dict['mime_obj']
            msg_related.attach(mime_obj)

        # RAWメール送信
        response = client.send_raw_email(
            Source=source,
            Destinations=to_addresses,
            RawMessage={
                'Data': msg_root.as_string()
            }
        )
        logger.info(f"メール送信成功（添付あり）: {subject} to {to_addresses}")
        print(f"メール送信成功: MessageId={response['MessageId']}")
        return True
        
    except Exception as e:
        logger.error(f"メール送信失敗: {e}")
        print(f"メール送信エラー: {e}")
        return False
