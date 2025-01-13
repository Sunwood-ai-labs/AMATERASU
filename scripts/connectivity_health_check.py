import socket
import requests
import dns.resolver
import subprocess
from typing import Dict, List
from datetime import datetime
from loguru import logger
import sys

# ロガーの設定
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | <level>{message}</level>",
    colorize=True
)

def check_dns_resolution(hostname: str) -> Dict:
    """DNS名前解決の詳細を確認する"""
    logger.info(f"DNSの名前解決を開始: {hostname}")
    
    try:
        # 標準的なSocket APIによる名前解決
        ip_addr = socket.gethostbyname(hostname)
        logger.debug(f"プライマリIPアドレス: {ip_addr}")
        
        # dns.resolverを使用したより詳細な情報取得
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['127.0.0.53']  # Local DNS resolver
        
        results = []
        for qtype in ['A', 'CNAME']:
            try:
                answers = resolver.resolve(hostname, qtype)
                for rdata in answers:
                    results.append({
                        'record_type': qtype,
                        'value': str(rdata)
                    })
                    logger.debug(f"DNSレコード検出: {qtype} => {str(rdata)}")
            except dns.resolver.NoAnswer:
                logger.debug(f"DNSレコードなし: {qtype}")
                continue
            
        logger.success("DNS名前解決が成功しました")
        return {
            'status': 'success',
            'primary_ip': ip_addr,
            'detailed_records': results
        }
    except Exception as e:
        logger.error(f"DNS名前解決でエラーが発生: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }

def check_http_connectivity(hostname: str) -> Dict:
    """HTTP接続確認を行う"""
    logger.info(f"HTTP接続確認を開始: {hostname}")
    
    try:
        url = f'http://{hostname}'
        response = requests.get(url, timeout=5)
        logger.success(f"HTTP接続成功: ステータスコード {response.status_code}")
        logger.debug(f"レスポンスサイズ: {len(response.text)} bytes")
        logger.debug(f"コンテンツタイプ: {response.headers.get('content-type', 'unknown')}")
        
        return {
            'status': 'success',
            'status_code': response.status_code,
            'response_size': len(response.text),
            'content_type': response.headers.get('content-type', 'unknown')
        }
    except Exception as e:
        logger.error(f"HTTP接続でエラーが発生: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }

def check_ping(hostname: str) -> Dict:
    """ICMP Pingによる疎通確認"""
    logger.info(f"PING確認を開始: {hostname}")
    
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '2', hostname],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'time=' in line:
                    time_ms = float(line.split('time=')[1].split()[0])
                    logger.success(f"PING成功: 応答時間 {time_ms}ms")
                    return {
                        'status': 'success',
                        'latency_ms': time_ms
                    }
        
        logger.warning("PINGが失敗しました")
        return {
            'status': 'error',
            'error': 'Ping failed'
        }
    except Exception as e:
        logger.error(f"PING実行でエラーが発生: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }

def check_host(hostname: str) -> Dict:
    """単一ホストの全チェックを実行"""
    logger.info(f"\n{'=' * 40} ホスト: {hostname} {'=' * 40}")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'hostname': hostname,
        'dns_check': check_dns_resolution(hostname),
        'ping_check': check_ping(hostname),
        'http_check': check_http_connectivity(hostname)
    }
    
    # 結果の判定
    all_success = all(v.get('status') == 'success' 
                     for v in [results['dns_check'], results['ping_check'], results['http_check']])
    
    if all_success:
        logger.success(f"ホスト {hostname} のすべての確認が成功")
    else:
        logger.error(f"ホスト {hostname} で一部問題を検出")
    
    return results

def main():
    # 検証するホストのリスト
    hosts = [
        "amaterasu-litellm.sunwood-ai-labs-internal.com",
        "amaterasu-open-web-ui.sunwood-ai-labs-internal.com"
        # 他のホストを追加可能
    ]
    
    logger.info(f"接続確認を開始します - 対象ホスト数: {len(hosts)}")
    all_results = []
    
    for hostname in hosts:
        result = check_host(hostname)
        all_results.append(result)
    
    # 総合結果の表示
    print("\n" + "=" * 80)
    total_success = all(
        all(v.get('status') == 'success' 
            for v in result.values() 
            if isinstance(v, dict) and 'status' in v)
        for result in all_results
    )
    
    if total_success:
        logger.success("すべてのホストの接続確認が成功しました")
    else:
        logger.error("一部のホストで問題が検出されました")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
