import asyncio
from loguru import logger
from app.core.lifecycle import lifespan
from app.core.logger import set_trace_id
from app.graph.workflow import app_workflow

async def main_async():
    # 1. 使用 lifespan 管理资源（startup/shutdown）
    async with lifespan():
        # 2. 为当前运行设置 Trace ID
        set_trace_id()
        logger.info("系统启动成功，进入主循环...")

        # 3. 工作流执行示例
        initial_state = {
            "messages": [("user", "你好，我需要一个计划。")],
            "next_step": "",
            "is_finished": False
        }
        
        async for event in app_workflow.astream(initial_state):
            for node_name, output in event.items():
                logger.info(f"节点 '{node_name}' 执行完毕并输出。")

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在退出...")

if __name__ == "__main__":
    main()
