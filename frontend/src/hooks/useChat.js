import { useState, useEffect, useRef } from 'react';

const useChat = (sessionId) => {
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    if (!sessionId) return;

    // WebSocket接続
    const wsUrl = `ws://localhost:8000/ws/chat/${sessionId}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    ws.current.onmessage = (event) => {
      const messageContent = event.data;
      
      // ストリーミングの終わりを判定
      if (messageContent === '[END_OF_STREAM]') {
        // 新しいアシスタントメッセージオブジェクトを追加する準備
        setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
      } else {
        setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
          // アシスタントの最後のメッセージにトークンを追記
          if (lastMessage && lastMessage.role === 'assistant') {
            const updatedMessages = [...prev];
            updatedMessages[prev.length - 1].content += messageContent;
            return updatedMessages;
          } else {
            // 新規アシスタントメッセージとして開始
             return [...prev, { role: 'assistant', content: messageContent }];
          }
        });
      }
    };

    // コンポーネントのアンマウント時に接続をクリーンアップ
    return () => {
      ws.current?.close();
    };
  }, [sessionId]);

  const sendMessage = (message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message);
      // ユーザーのメッセージをメッセージリストに追加
      setMessages(prev => [...prev, { role: 'user', content: message }]);
    }
  };

  return { messages, sendMessage, isConnected };
};

export default useChat;