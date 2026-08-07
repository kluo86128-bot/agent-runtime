# app/db/db_conn_status.py
from typing import Dict, Any
from sqlalchemy.pool import NullPool
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def get_pool_status(pool, session=None) -> Dict[str, Any]:
    """
    获取数据库连接池的状态信息
    """
    if not pool:
        return {
            'error': '连接池对象为空',
        }
    
    try:
        # 检查是否为 NullPool (SQLite)
        if isinstance(pool, NullPool) or not hasattr(pool, 'size'):
            # 尝试通过 session 获取 SQLite 连接信息
            status = {
                'pool_type': 'NullPool (SQLite)',
                'note': 'SQLite 无连接池限制',
            }
            
            # 如果有 session，获取 SQLite 运行时信息
            if session:
                try:
                    # 获取当前连接数（SQLite 不直接支持，但可以获取连接状态）
                    result = session.execute(text("PRAGMA database_list"))
                    databases = result.fetchall()
                    status['databases'] = [dict(db._mapping) for db in databases]
                    
                    # 获取编译指示信息
                    result = session.execute(text("PRAGMA compile_options"))
                    compile_options = result.fetchall()
                    status['compile_options'] = [opt[0] for opt in compile_options]
                    
                    # 获取连接ID（如果有）
                    try:
                        result = session.execute(text("SELECT connection_id()"))
                        conn_id = result.fetchone()
                        if conn_id:
                            status['connection_id'] = conn_id[0]
                    except:
                        pass
                    
                    # 检查是否有其他连接（通过锁状态）
                    try:
                        result = session.execute(text("PRAGMA lock_status"))
                        locks = result.fetchall()
                        if locks:
                            status['locks'] = [dict(lock._mapping) for lock in locks]
                    except:
                        pass
                    
                except Exception as e:
                    logger.debug(f"获取 SQLite 运行时信息失败: {e}")
                    status['note'] = '无法获取 SQLite 运行时信息'
            
            return {
                'status': status,
                'health': {
                    'is_healthy': True,
                    'warnings': ['SQLite 使用 NullPool，每次创建新连接']
                },
                'error': None
            }
        
        # 如果是其他类型的 pool（QueuePool 等）
        if hasattr(pool, 'size') and callable(pool.size):
            size = pool.size()
            checkedout = pool.checkedout() if hasattr(pool, 'checkedout') else 0
            checkedin = pool.checkedin() if hasattr(pool, 'checkedin') else 0
            overflow = pool.overflow() if hasattr(pool, 'overflow') else 0
            
            total = size + overflow
            utilization = (checkedout / total * 100) if total > 0 else 0
            
            return {
                'status': {
                    'pool_type': type(pool).__name__,
                    'pool_size': size,
                    'checked_out': checkedout,
                    'checked_in': checkedin,
                    'overflow': overflow,
                    'total_connections': total,
                    'utilization': round(utilization, 2),
                },
                'health': {
                    'is_healthy': utilization < 80,
                    'warnings': [f'使用率过高: {utilization:.1f}%'] if utilization >= 80 else []
                },
                'error': None
            }
        
        # 未知类型的 pool
        return {
            'status': {
                'pool_type': str(type(pool)),
                'note': '未知连接池类型',
            },
            'health': {
                'is_healthy': True,
                'warnings': []
            },
            'error': None
        }
        
    except Exception as e:
        logger.error(f"获取连接池状态失败: {e}")
        return {
            'error': str(e),
            'status': {},
            'health': {
                'is_healthy': False,
                'warnings': [f'获取状态异常: {str(e)}']
            }
        }


def print_pool_status(pool, session=None, title: str = "数据库连接池状态"):
    """打印格式化的连接池状态"""
    status = get_pool_status(pool, session)
    
    if status.get('error'):
        print(f"\n❌ {title}")
        print(f"错误: {status['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    
    s = status['status']
    
    # SQLite NullPool
    if s.get('pool_type') == 'NullPool (SQLite)':
        print("🔍 数据库类型: SQLite (NullPool模式)")
        print(f"   说明: {s.get('note', '无连接池限制')}")
        
        # 显示数据库信息
        if 'databases' in s:
            print(f"\n   📁 数据库文件:")
            for db in s['databases']:
                print(f"      - {db.get('name', 'unknown')}: {db.get('file', 'memory')}")
        
        # 显示连接信息
        if 'connection_id' in s:
            print(f"\n   🔗 连接ID: {s['connection_id']}")
        
        # 显示编译选项
        if 'compile_options' in s:
            print(f"\n   ⚙️ 编译选项: {', '.join(s['compile_options'][:5])}")
            if len(s['compile_options']) > 5:
                print(f"      ... 还有 {len(s['compile_options']) - 5} 个选项")
        
        # 显示锁状态
        if 'locks' in s and s['locks']:
            print(f"\n   🔒 锁状态:")
            for lock in s['locks']:
                print(f"      - {lock}")
        
        print(f"\n   💡 提示: SQLite 无连接池限制，但写操作是串行的")
        print(f"{'='*60}\n")
        return
    
    # 其他连接池显示
    if 'pool_size' in s:
        print(f"连接池类型:          {s.get('pool_type', 'Unknown')}")
        print(f"连接池大小:          {s.get('pool_size', 0)}")
        print(f"当前借出连接:        {s.get('checked_out', 0)}")
        print(f"当前空闲连接:        {s.get('checked_in', 0)}")
        print(f"溢出连接数:          {s.get('overflow', 0)}")
        print(f"总连接数:            {s.get('total_connections', 0)}")
        print(f"连接使用率:          {s.get('utilization', 0):.1f}%")
    
    health = status.get('health', {})
    if health.get('is_healthy', False):
        print(f"\n✅ 健康状态: 正常")
    else:
        print(f"\n⚠️ 健康状态: 异常")
        warnings = health.get('warnings', [])
        if warnings:
            print(f"警告:")
            for warning in warnings:
                print(f"  - {warning}")
    
    print(f"{'='*60}\n")


def log_pool_status(pool, session=None, title: str = "数据库连接池状态"):
    """将连接池状态记录到日志"""
    status = get_pool_status(pool, session)
    
    if status.get('error'):
        logger.error(f"{title} - 连接池状态获取失败: {status['error']}")
        return
    
    s = status['status']
    
    # SQLite NullPool
    if s.get('pool_type') == 'NullPool (SQLite)':
        log_msg = f"{title} - SQLite 使用 NullPool"
        if 'databases' in s:
            db_names = [db.get('name', 'unknown') for db in s['databases']]
            log_msg += f", 数据库: {', '.join(db_names)}"
        if 'connection_id' in s:
            log_msg += f", 连接ID: {s['connection_id']}"
        logger.info(log_msg)
        return
    
    # 其他连接池
    if 'total_connections' in s:
        logger.info(
            f"{title} - 连接池状态: "
            f"已用={s.get('checked_out', 0)}/{s.get('total_connections', 0)} "
            f"空闲={s.get('checked_in', 0)} "
            f"使用率={s.get('utilization', 0):.1f}%"
        )
    else:
        logger.info(f"{title} - {s}")


def get_pool_snapshot(pool, session=None) -> str:
    """获取连接池状态的简略字符串"""
    status = get_pool_status(pool, session)
    
    if status.get('error'):
        return f"[连接池异常: {status['error']}]"
    
    s = status['status']
    
    if s.get('pool_type') == 'NullPool (SQLite)':
        base = "[SQLite NullPool"
        if 'connection_id' in s:
            base += f" - conn:{s['connection_id']}"
        if 'databases' in s:
            db_files = [db.get('file', 'memory') for db in s['databases']]
            base += f" - db:{', '.join(db_files)}"
        return base + "]"
    
    if 'total_connections' in s:
        return (
            f"已用={s.get('checked_out', 0)}/{s.get('total_connections', 0)} "
            f"使用率={s.get('utilization', 0):.1f}%"
        )
    
    return str(s)


def is_pool_exhausted(pool, session=None, threshold: float = 0.8) -> bool:
    """检查连接池是否即将耗尽（SQLite 永远返回 False）"""
    status = get_pool_status(pool, session)
    if status.get('error'):
        return False
    
    s = status['status']
    
    # SQLite NullPool 永远不会耗尽
    if s.get('pool_type') == 'NullPool (SQLite)':
        return False
    
    # 其他连接池检查
    if 'utilization' in s:
        return s['utilization'] > threshold
    
    return False


def get_available_connections(pool, session=None) -> int:
    """获取当前可用的连接数"""
    status = get_pool_status(pool, session)
    if status.get('error'):
        return 0
    
    s = status['status']
    if s.get('pool_type') == 'NullPool (SQLite)':
        return -1  # 无限制
    
    return s.get('checked_in', 0)