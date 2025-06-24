# 第一阶段：构建应用
FROM node:18-alpine AS builder

WORKDIR /app

# 安装pnpm
RUN npm install -g pnpm

# 设置npm镜像源以提高下载速度
RUN npm config set registry https://registry.npmmirror.com/

# 复制package文件
COPY package*.json pnpm-lock.yaml* ./

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

# 设置环境变量
ENV NODE_ENV=production
ENV REACT_APP_API_URL=/api/v1
ENV GENERATE_SOURCEMAP=false
ENV CI=false

# 构建应用
RUN pnpm build

# 第二阶段：运行nginx服务器
FROM nginx:alpine

# 安装curl用于健康检查
RUN apk add --no-cache curl

# 删除默认的nginx配置和文件
RUN rm -rf /usr/share/nginx/html/*
RUN rm /etc/nginx/conf.d/default.conf

# 复制构建好的应用
COPY --from=builder /app/build /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 设置正确的权限
RUN chmod -R 755 /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]