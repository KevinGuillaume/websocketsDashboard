import { useState, useEffect, useRef, useCallback} from 'react'

export function usePriceSocket() {
    const [prices, setPrices] = useState({});
    const [status, setStatus] = useState("disconnected");
    const wsRef = useRef(null);
    const reconnectTimer = useRef(null);

    const connect = useCallback(() => {
        console.log("connect() called, readyState:", wsRef.current?.readyState);

        if (
            wsRef.current &&
            (wsRef.current.readyState === WebSocket.CONNECTING ||
            wsRef.current.readyState === WebSocket.CLOSING)    // ← add this
        ) {
            console.log("socket busy, bailing");
            return;
        }

        const ws = new WebSocket("ws://localhost:8100/ws/prices");
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("connected");
            setStatus("connected");
        };

        ws.onmessage = (event) => {
            console.log("raw message:", event.data)
            const { symbol, price } = JSON.parse(event.data);
            setPrices(prev => ({ ...prev, [symbol]: price }));
        };

        ws.onerror = (error) => {
            console.log("error:", error);
            setStatus("error");
        };

        ws.onclose = (event) => {
            console.log("closed, code:", event.code, "reason:", event.reason);
            setStatus("disconnected");
            reconnectTimer.current = setTimeout(connect, 3000);
        };
        }, []);


    useEffect(() => {
        connect();

        return () => {
            clearTimeout(reconnectTimer.current);
            wsRef.current?.close();
        }

    },[connect]);

    return { prices, status };
}