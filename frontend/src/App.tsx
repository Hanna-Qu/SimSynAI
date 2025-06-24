import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { ConfigProvider, Layout, Menu, Button, Select, message, Dropdown, Avatar, Spin } from 'antd';
import { UserOutlined, LockOutlined, ExperimentOutlined, AreaChartOutlined, MenuOutlined, DashboardOutlined, MessageOutlined } from '@ant-design/icons';
import zhCN from 'antd/lib/locale/zh_CN';
import enUS from 'antd/lib/locale/en_US';
import { useTranslation } from 'react-i18next';
import './App.css';
import './styles/auth.css';
import './styles/layout.css';
import { useMediaQuery } from 'react-responsive';

// 导入组件
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/Dashboard';
import Chat from './components/Chat';
import Simulation from './components/Simulation';
import Visualization from './components/Visualization';
import Profile from './components/Profile';

const { Header, Content, Sider } = Layout;
const { Option } = Select;

// 类型定义
interface User {
  username: string;
  email?: string;
  full_name?: string;
}

interface LoginData {
  username: string;
  password: string;
}

// 主应用组件
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [collapsed, setCollapsed] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const { t, i18n } = useTranslation();
  const isMobile = useMediaQuery({ maxWidth: 768 });

  // 验证token有效性
  const validateToken = async (token: string): Promise<boolean> => {
    try {
      const response = await fetch('/api/v1/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const userData = await response.json();
        setCurrentUser(userData);
        return true;
      } else {
        // Token无效，清除本地存储
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        return false;
      }
    } catch (error) {
      console.error('Token验证失败:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      return false;
    }
  };

  // 检查认证状态
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      const username = localStorage.getItem('username');
      
      if (token && username) {
        const isValid = await validateToken(token);
        if (isValid) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
          setCurrentUser(null);
        }
      } else {
        setIsAuthenticated(false);
        setCurrentUser(null);
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  // 初始化语言设置
  useEffect(() => {
    const savedLanguage = localStorage.getItem('language');
    if (savedLanguage && (savedLanguage === 'zh' || savedLanguage === 'en')) {
      i18n.changeLanguage(savedLanguage);
    }
  }, [i18n]);

  // 登录处理
  const handleLogin = async (loginData: LoginData) => {
    try {
      // 登录成功后重新获取用户信息
      const token = localStorage.getItem('token');
      if (token) {
        await validateToken(token);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('登录处理错误:', error);
      message.error('登录失败');
    }
  };

  // 注册处理
  const handleRegister = async (registerData: any) => {
    try {
      // 注册成功后不自动登录，跳转到登录页
      message.success('注册成功，请登录');
    } catch (error) {
      console.error('注册处理错误:', error);
      message.error('注册失败');
    }
  };

  // 登出处理
  const handleLogout = async () => {
    try {
      // 清除所有本地存储
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      localStorage.removeItem('remember');
      
      // 重置状态
      setIsAuthenticated(false);
      setCurrentUser(null);
      
      message.success(t('user.logoutSuccess') || '已成功登出');
      
      // 强制刷新页面以清除所有状态
      window.location.href = '/login';
    } catch (error) {
      console.error('登出错误:', error);
      message.error('登出失败');
    }
  };

  // 语言切换
  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
    // 强制重新渲染以更新所有组件的翻译
    window.location.reload();
  };

  // 受保护的路由组件
  const ProtectedRoute = ({ children }: { children: React.ReactNode }): JSX.Element => {
    const location = useLocation();
    
    if (!isAuthenticated) {
      return <Navigate to="/login" state={{ from: location }} replace />;
    }
    
    return <>{children}</>;
  };

  // 主布局组件
  const MainLayout = ({ children }: { children: React.ReactNode }) => {
    const navigate = useNavigate();
    const location = useLocation();
    
    // 根据当前路径设置选中的菜单项
    const getSelectedKey = () => {
      const path = location.pathname;
      if (path.includes('/dashboard')) return 'dashboard';
      if (path.includes('/chat')) return 'chat';
      if (path.includes('/simulation')) return 'simulation';
      if (path.includes('/visualization')) return 'visualization';
      return 'dashboard';
    };
    
    const menuItems = [
      {
        key: 'dashboard',
        icon: <DashboardOutlined />,
        label: t('menu.dashboard') || '仪表板',
        onClick: () => navigate('/dashboard')
      },
      {
        key: 'chat',
        icon: <MessageOutlined />,
        label: t('menu.chat') || '智能对话',
        onClick: () => navigate('/chat')
      },
      {
        key: 'simulation',
        icon: <ExperimentOutlined />,
        label: t('menu.simulation') || '仿真实验',
        onClick: () => navigate('/simulation')
      },
      {
        key: 'visualization',
        icon: <AreaChartOutlined />,
        label: t('menu.visualization') || '数据可视化',
        onClick: () => navigate('/visualization')
      }
    ];

    const userMenu = (
      <Menu>
        <Menu.Item key="profile" icon={<UserOutlined />} onClick={() => navigate('/profile')}>
          {t('user.profile') || '个人资料'}
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item key="logout" icon={<LockOutlined />} onClick={handleLogout}>
          {t('user.logout') || '退出登录'}
        </Menu.Item>
      </Menu>
    );

    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Sider 
          collapsible 
          collapsed={collapsed} 
          onCollapse={setCollapsed}
          breakpoint="lg"
          collapsedWidth={isMobile ? 0 : 80}
          style={{
            background: '#001529'
          }}
        >
          <div className="logo" style={{
            height: '32px',
            margin: '16px',
            background: 'rgba(255, 255, 255, 0.3)',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold'
          }}>
            {collapsed ? 'S' : 'SimSynAI'}
          </div>
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[getSelectedKey()]}
            items={menuItems}
            style={{ border: 'none' }}
          />
        </Sider>
        
        <Layout>
          <Header style={{
            padding: '0 16px',
            background: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 1px 4px rgba(0,21,41,.08)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <Button
                type="text"
                icon={<MenuOutlined />}
                onClick={() => setCollapsed(!collapsed)}
                style={{ fontSize: '16px', width: 64, height: 64 }}
              />
              <h1 style={{ margin: 0, fontSize: '18px', color: '#001529' }}>
                {t('common.title') || 'SimSynAI - 智能化仿真平台'}
              </h1>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Select
                value={i18n.language}
                style={{ width: 100 }}
                onChange={changeLanguage}
                size="small"
              >
                <Option value="zh">中文</Option>
                <Option value="en">English</Option>
              </Select>
              
              <Dropdown overlay={userMenu} placement="bottomRight">
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  cursor: 'pointer',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  transition: 'background-color 0.3s'
                }}>
                  <Avatar size="small" icon={<UserOutlined />} style={{ marginRight: '8px' }} />
                  <span>{currentUser?.username || 'User'}</span>
                </div>
              </Dropdown>
            </div>
          </Header>
          
          <Content style={{
            margin: '16px',
            padding: '16px',
            background: '#fff',
            borderRadius: '6px',
            minHeight: 'calc(100vh - 112px)',
            overflow: 'auto'
          }}>
            {children}
          </Content>
        </Layout>
      </Layout>
    );
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh'
      }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <ConfigProvider locale={i18n.language === 'zh' ? zhCN : enUS}>
      <Router>
    <div className="App">
          <Routes>
            {/* 公开路由 */}
            <Route 
              path="/login" 
              element={
                isAuthenticated ? 
                <Navigate to="/dashboard" replace /> : 
                <Login onLogin={handleLogin} />
              } 
            />
            <Route 
              path="/register" 
              element={
                isAuthenticated ? 
                <Navigate to="/dashboard" replace /> : 
                <Register onRegister={handleRegister} />
              } 
            />
            
            {/* 受保护的路由 */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <Dashboard />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/chat"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <Chat />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/simulation"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <Simulation />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            
            <Route 
              path="/visualization" 
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <Visualization />
                  </MainLayout>
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <Profile />
                  </MainLayout>
                </ProtectedRoute>
              } 
            />
            
            {/* 默认重定向 */}
            <Route 
              path="/" 
              element={
                <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />
              } 
            />
            
            {/* 404页面 */}
            <Route 
              path="*" 
              element={
                <div style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100vh'
                }}>
                  <h1>404</h1>
                  <p>{t('common.pageNotFound') || '页面未找到'}</p>
                  <Button type="primary" onClick={() => window.location.href = '/'}>
                    {t('common.backHome') || '返回首页'}
                  </Button>
                </div>
              } 
            />
          </Routes>
    </div>
      </Router>
    </ConfigProvider>
  );
}

export default App;