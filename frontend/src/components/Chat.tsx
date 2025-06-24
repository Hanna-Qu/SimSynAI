import React, { useState, useEffect, useRef } from 'react';
import { Card, Input, Button, Select, List, Avatar, message, Spin, Tag, Space, Alert } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined, ClearOutlined, SettingOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

const { TextArea } = Input;
const { Option } = Select;

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  model?: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('openai');
  const [apiKeyError, setApiKeyError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { t } = useTranslation();
  const navigate = useNavigate();

  const models = [
    { value: 'openai', label: 'OpenAI GPT', color: 'blue' },
    { value: 'anthropic', label: 'Claude', color: 'green' },
    { value: 'google', label: 'Gemini', color: 'red' },
    { value: 'qwen', label: t('chat.models.qwen') || '通义千问', color: 'orange' },
    { value: 'deepseek', label: 'DeepSeek', color: 'purple' }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    setApiKeyError(null);

    try {
      const response = await fetch('/api/v1/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          message: inputValue,
          model: selectedModel
        })
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: data.response || t('chat.noResponse') || '抱歉，我现在无法回答您的问题。',
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          model: selectedModel
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorData = await response.json();
        if (response.status === 400 && errorData.detail?.includes('API密钥')) {
          setApiKeyError(errorData.detail);
        } else {
          message.error(t('chat.sendError') || '发送消息失败，请重试');
        }
        
        // 添加错误消息
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: t('chat.errorResponse') || '抱歉，我现在无法回答您的问题。请检查API密钥配置或稍后重试。',
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          model: selectedModel
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      message.error(t('common.networkError') || '网络错误，请检查连接');
      // 添加错误消息
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: t('chat.networkError') || '抱歉，我现在无法回答您的问题。请检查网络连接或稍后重试。',
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        model: selectedModel
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = () => {
    setMessages([]);
    setApiKeyError(null);
    message.success(t('chat.historyCleared') || '对话历史已清空');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getCurrentModel = () => {
    return models.find(model => model.value === selectedModel);
  };

  const goToProfile = () => {
    navigate('/profile');
  };

  return (
    <div style={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
      {/* API密钥错误提示 */}
      {apiKeyError && (
        <Alert
          message={t('chat.noApiKey') || '请先配置API密钥'}
          description={
            <div>
              {apiKeyError}
              <br />
              <Button 
                type="link" 
                icon={<SettingOutlined />}
                onClick={goToProfile}
                style={{ padding: 0, marginTop: 8 }}
              >
                {t('chat.configureApiKey') || '点击前往个人设置配置API密钥'}
              </Button>
            </div>
          }
          type="warning"
          showIcon
          closable
          onClose={() => setApiKeyError(null)}
          style={{ marginBottom: 16 }}
        />
      )}

      {/* 头部控制栏 */}
      <Card size="small" style={{ marginBottom: 16 }}>
        <Space>
          <span>{t('chat.selectModel') || '选择模型'}：</span>
          <Select
            value={selectedModel}
            onChange={setSelectedModel}
            style={{ width: 200 }}
          >
            {models.map(model => (
              <Option key={model.value} value={model.value}>
                <Tag color={model.color}>{model.label}</Tag>
              </Option>
            ))}
          </Select>
          <Button 
            icon={<ClearOutlined />} 
            onClick={clearHistory}
            disabled={messages.length === 0}
          >
            {t('chat.clearHistory') || '清空历史'}
          </Button>
        </Space>
      </Card>

      {/* 对话区域 */}
      <Card 
        title={
          <Space>
            <RobotOutlined />
            <span>{t('chat.title') || 'AI助手对话'}</span>
            <Tag color={getCurrentModel()?.color}>
              {getCurrentModel()?.label}
            </Tag>
          </Space>
        }
        style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
        bodyStyle={{ flex: 1, display: 'flex', flexDirection: 'column', padding: 0 }}
      >
        {/* 消息列表 */}
        <div 
          style={{ 
            flex: 1, 
            overflowY: 'auto', 
            padding: '16px',
            backgroundColor: '#fafafa'
          }}
        >
          {messages.length === 0 ? (
            <div style={{ 
              textAlign: 'center', 
              color: '#999', 
              marginTop: '50px' 
            }}>
              <RobotOutlined style={{ fontSize: 48, marginBottom: 16 }} />
              <p>{t('chat.greeting') || '您好！我是AI助手，可以帮助您进行仿真配置和结果分析。'}</p>
              <p>{t('chat.startConversation') || '请选择模型并开始对话。'}</p>
            </div>
          ) : (
            <List
              dataSource={messages}
              renderItem={(message) => (
                <List.Item style={{ border: 'none', padding: '8px 0' }}>
                  <div style={{ 
                    width: '100%',
                    display: 'flex',
                    justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start'
                  }}>
                    <div style={{
                      maxWidth: '70%',
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '8px',
                      flexDirection: message.sender === 'user' ? 'row-reverse' : 'row'
                    }}>
                      <Avatar 
                        icon={message.sender === 'user' ? <UserOutlined /> : <RobotOutlined />}
                        style={{ 
                          backgroundColor: message.sender === 'user' ? '#1890ff' : '#52c41a',
                          flexShrink: 0
                        }}
                      />
                      <div style={{
                        backgroundColor: message.sender === 'user' ? '#1890ff' : '#fff',
                        color: message.sender === 'user' ? '#fff' : '#000',
                        padding: '12px 16px',
                        borderRadius: '12px',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                        wordBreak: 'break-word'
                      }}>
                        <div style={{ marginBottom: '4px' }}>
                          {message.content}
                        </div>
                        <div style={{ 
                          fontSize: '12px', 
                          opacity: 0.7,
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          marginTop: '8px'
                        }}>
                          <span>{message.timestamp}</span>
                          {message.model && message.sender === 'assistant' && (
                            <Tag color={getCurrentModel()?.color} style={{ fontSize: '11px' }}>
                              {getCurrentModel()?.label}
                            </Tag>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </List.Item>
              )}
            />
          )}
          {loading && (
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <Spin />
              <div style={{ marginTop: '8px', color: '#999' }}>
                {t('chat.thinking') || 'AI正在思考中...'}
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 输入区域 */}
        <div style={{ 
          padding: '16px', 
          borderTop: '1px solid #f0f0f0',
          backgroundColor: '#fff'
        }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            <TextArea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={t('chat.placeholder') || '请输入您的问题...'}
              autoSize={{ minRows: 1, maxRows: 4 }}
              disabled={loading}
              style={{ flex: 1 }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={sendMessage}
              disabled={loading || !inputValue.trim()}
              style={{ height: 'auto' }}
            >
              {t('chat.sendMessage') || '发送'}
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Chat; 