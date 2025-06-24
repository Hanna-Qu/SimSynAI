import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Tabs, 
  Form, 
  Input, 
  Button, 
  message, 
  Select, 
  Space, 
  Typography, 
  Divider,
  Alert,
  Badge,
  Spin
} from 'antd';
import {
  UserOutlined,
  LockOutlined,
  KeyOutlined,
  MailOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import { useTranslation } from 'react-i18next';

const { Title, Text } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;

interface UserProfile {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  preferred_model?: string;
  is_active: boolean;
}

interface APIKeyStatus {
  openai: boolean;
  anthropic: boolean;
  google: boolean;
  qwen: boolean;
  deepseek: boolean;
}

const Profile: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [profileLoading, setProfileLoading] = useState(true);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [apiKeyStatus, setApiKeyStatus] = useState<APIKeyStatus>({
    openai: false,
    anthropic: false,
    google: false,
    qwen: false,
    deepseek: false
  });
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();
  const [apiKeyForm] = Form.useForm();

  // 获取用户资料
  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        message.error('请先登录');
        return;
      }

      const response = await fetch('/api/v1/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUserProfile(data);
        form.setFieldsValue({
          username: data.username,
          email: data.email,
          full_name: data.full_name || '',
          preferred_model: data.preferred_model || 'openai'
        });
      } else {
        message.error('获取用户信息失败');
      }
    } catch (error) {
      console.error('获取用户信息错误:', error);
      message.error('获取用户信息失败');
    } finally {
      setProfileLoading(false);
    }
  };

  // 获取API密钥状态
  const fetchAPIKeyStatus = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch('/api/v1/users/api-keys/status', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setApiKeyStatus(data);
      }
    } catch (error) {
      console.error('获取API密钥状态错误:', error);
    }
  };

  useEffect(() => {
    fetchUserProfile();
    fetchAPIKeyStatus();
  }, []);

  // 更新基本信息
  const handleUpdateProfile = async (values: any) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/users/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(values)
      });

      if (response.ok) {
        message.success('个人信息更新成功');
        await fetchUserProfile();
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || '更新失败');
      }
    } catch (error) {
      message.error('更新失败，请稍后再试');
    } finally {
      setLoading(false);
    }
  };

  // 修改密码
  const handleChangePassword = async (values: any) => {
    if (values.new_password !== values.confirm_password) {
      message.error('两次输入的密码不一致');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/users/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: values.current_password,
          new_password: values.new_password
        })
      });

      if (response.ok) {
        message.success('密码修改成功');
        passwordForm.resetFields();
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || '密码修改失败');
      }
    } catch (error) {
      message.error('密码修改失败，请稍后再试');
    } finally {
      setLoading(false);
    }
  };

  // 更新API密钥
  const handleUpdateAPIKey = async (provider: string, apiKey: string) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/users/api-keys', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          [provider]: apiKey
        })
      });

      if (response.ok) {
        message.success(`${provider.toUpperCase()} API密钥更新成功`);
        await fetchAPIKeyStatus();
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || 'API密钥更新失败');
      }
    } catch (error) {
      message.error('API密钥更新失败，请稍后再试');
    } finally {
      setLoading(false);
    }
  };

  // 测试API密钥连接
  const handleTestAPIKey = async (provider: string) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/v1/users/api-keys/test/${provider}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        message.success(`${provider.toUpperCase()} API连接测试成功`);
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || 'API连接测试失败');
      }
    } catch (error) {
      message.error('API连接测试失败，请稍后再试');
    } finally {
      setLoading(false);
    }
  };

  if (profileLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px' 
      }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
      <Title level={2}>
        <UserOutlined /> {t('profile.title') || '个人资料'}
      </Title>
      
      <Card>
        <Tabs defaultActiveKey="basic">
          <TabPane tab={t('profile.basicInfo') || '基本信息'} key="basic">
            <Form
              form={form}
              layout="vertical"
              onFinish={handleUpdateProfile}
            >
              <Form.Item
                label={t('profile.username') || '用户名'}
                name="username"
                rules={[{ required: true, message: '请输入用户名' }]}
              >
                <Input disabled prefix={<UserOutlined />} />
              </Form.Item>

              <Form.Item
                label={t('profile.email') || '邮箱'}
                name="email"
                rules={[
                  { required: true, message: '请输入邮箱' },
                  { type: 'email', message: '请输入有效的邮箱地址' }
                ]}
              >
                <Input prefix={<MailOutlined />} />
              </Form.Item>

              <Form.Item
                label={t('profile.fullName') || '全名'}
                name="full_name"
              >
                <Input prefix={<UserOutlined />} />
              </Form.Item>

              <Form.Item
                label={t('profile.preferredModel') || '首选模型'}
                name="preferred_model"
              >
                <Select>
                  <Option value="openai">OpenAI GPT</Option>
                  <Option value="anthropic">Anthropic Claude</Option>
                  <Option value="google">Google Gemini</Option>
                  <Option value="qwen">阿里千问</Option>
                  <Option value="deepseek">DeepSeek</Option>
                </Select>
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  {t('profile.updateProfile') || '更新资料'}
                </Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane tab={t('profile.changePassword') || '修改密码'} key="password">
            <Form
              form={passwordForm}
              layout="vertical"
              onFinish={handleChangePassword}
            >
              <Form.Item
                label={t('profile.currentPassword') || '当前密码'}
                name="current_password"
                rules={[{ required: true, message: '请输入当前密码' }]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item
                label={t('profile.newPassword') || '新密码'}
                name="new_password"
                rules={[
                  { required: true, message: '请输入新密码' },
                  { min: 6, message: '密码长度至少为6个字符' }
                ]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item
                label={t('profile.confirmPassword') || '确认新密码'}
                name="confirm_password"
                rules={[{ required: true, message: '请确认新密码' }]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  {t('profile.changePassword') || '修改密码'}
                </Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane tab={t('profile.apiKeys') || 'API密钥管理'} key="apikeys">
            <Alert
              message={t('profile.apiKeyNotice') || 'API密钥安全提醒'}
              description={t('profile.apiKeyDescription') || '您的API密钥将被加密存储，仅用于您的AI对话服务。请妥善保管您的密钥，不要与他人分享。'}
              type="info"
              showIcon
              style={{ marginBottom: 24 }}
            />

            <Space direction="vertical" style={{ width: '100%' }} size="large">
              {[
                { key: 'openai', name: 'OpenAI', placeholder: 'sk-...' },
                { key: 'anthropic', name: 'Anthropic', placeholder: 'sk-ant-...' },
                { key: 'google', name: 'Google', placeholder: 'AIza...' },
                { key: 'qwen', name: '阿里千问', placeholder: 'sk-...' },
                { key: 'deepseek', name: 'DeepSeek', placeholder: 'sk-...' }
              ].map(provider => (
                <Card key={provider.key} size="small">
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ flex: 1 }}>
                      <Space>
                        <KeyOutlined />
                        <Text strong>{provider.name}</Text>
                        <Badge 
                          status={apiKeyStatus[provider.key as keyof APIKeyStatus] ? 'success' : 'default'}
                          text={apiKeyStatus[provider.key as keyof APIKeyStatus] ? '已配置' : '未配置'}
                        />
                      </Space>
                      <div style={{ marginTop: 8 }}>
                        <Input.Password
                          placeholder={provider.placeholder}
                          style={{ width: 300, marginRight: 8 }}
                          onChange={(e) => {
                            apiKeyForm.setFieldsValue({ [provider.key]: e.target.value });
                          }}
                        />
                        <Button
                          type="primary"
                          size="small"
                          loading={loading}
                          onClick={() => {
                            const value = apiKeyForm.getFieldValue(provider.key);
                            if (value) {
                              handleUpdateAPIKey(provider.key, value);
                            } else {
                              message.warning('请输入API密钥');
                            }
                          }}
                        >
                          更新
                        </Button>
                        {apiKeyStatus[provider.key as keyof APIKeyStatus] && (
                          <Button
                            size="small"
                            style={{ marginLeft: 8 }}
                            loading={loading}
                            onClick={() => handleTestAPIKey(provider.key)}
                          >
                            测试连接
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </Space>
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default Profile; 