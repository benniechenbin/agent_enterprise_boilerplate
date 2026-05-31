import asyncio
from loguru import logger
from app.core.lifecycle import lifespan
from app.core.logger import set_trace_id
from app.graph.workflow import create_workflow
from app.core.container import container

async def main_async():
    # 1. 使用 lifespan 管理资源（startup/shutdown）
    async with lifespan():
        # 2. 为当前运行设置 Trace ID
        set_trace_id()
        logger.info("系统启动成功，进入主循环...")

        # 3. 工作流执行示例 (使用实验室策略)
        # 策略模式：根据需求选择不同的工作流版本
        lab_workflow = create_workflow(strategy="lab")
        
        # 依赖注入：显式传入 llm_service，方便测试和多模型切换
        config = {
            "configurable": {
                "llm_service": container.get_llm()
            }
        }

        initial_state = {
            "messages": [("user", "任务：调研 2024 年大模型领域的最新突破。")],
            "next_step": "",
            "is_finished": False
        }
        
        logger.info("开始执行实验室版 (Lab) 多智能体流水线...")
        async for event in lab_workflow.astream(initial_state, config=config):
            for node_name, output in event.items():
                logger.info(f"节点 '{node_name}' 执行完毕。")
                if "messages" in output:
                    last_msg = output["messages"][-1]
                    logger.debug(f"节点反馈: {last_msg.content if hasattr(last_msg, 'content') else last_msg[1]}")

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在退出...")

if __name__ == "__main__":
    main()
