"""API路由注册模块

负责集中管理和注册所有API路由。每个功能模块的路由都被注册到相应的URL前缀下，
并通过tags进行分类，便于API文档的组织和查看。

路由分类：
- auth: 认证相关API
- users: 用户管理相关API
- chat: AI对话相关API
- simulation: 仿真任务相关API
- visualization: 数据可视化相关API
- models: 模型管理相关API
"""

from fastapi import APIRouter

from app.api.endpoints import auth, users, chat, simulation, visualization, models

api_router = APIRouter()

# 认证相关路由
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

# 用户管理路由
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

# AI对话路由
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
)

# 仿真任务路由
api_router.include_router(
    simulation.router,
    prefix="/simulation",
    tags=["simulation"]
)

# 数据可视化路由
api_router.include_router(
    visualization.router,
    prefix="/visualization",
    tags=["visualization"]
)

# 模型管理路由
api_router.include_router(
    models.router,
    prefix="/models",
    tags=["models"]
)