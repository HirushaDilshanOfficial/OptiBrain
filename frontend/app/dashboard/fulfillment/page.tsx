"use client"

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function FulfillmentPage() {
    const [orders, setOrders] = useState<any[]>([]);
    const [nodes, setNodes] = useState<any[]>([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchOrders();
        fetchNodes(); // Assuming we might want to list nodes too
    }, []);

    const fetchOrders = async () => {
        try {
            const response = await api.get('/api/v1/fulfillment/orders');
            setOrders(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchNodes = async () => {
        // Placeholder if we had a GET /nodes endpoint, otherwise skip
    };

    const routeOrder = async (orderId: number) => {
        try {
            await api.post('/api/v1/fulfillment/route', { order_id: orderId });
            setMessage(`Order ${orderId} routed successfully!`);
            fetchOrders();
        } catch (error) {
            console.error(error);
            setMessage('Routing failed.');
        }
    };

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Fulfillment Dashboard</h2>

            <Card>
                <CardHeader>
                    <CardTitle>Incoming Orders</CardTitle>
                </CardHeader>
                <CardContent>
                    {message && <p className="text-sm text-green-600 mb-4">{message}</p>}
                    <div className="relative w-full overflow-auto">
                        <table className="w-full caption-bottom text-sm">
                            <thead className="[&_tr]:border-b">
                                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Order ID</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">External ID</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">SKU</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Status</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Node ID</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Action</th>
                                </tr>
                            </thead>
                            <tbody className="[&_tr:last-child]:border-0">
                                {orders.map((order) => (
                                    <tr key={order.id} className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                        <td className="p-4 align-middle font-medium">{order.id}</td>
                                        <td className="p-4 align-middle">{order.external_order_id}</td>
                                        <td className="p-4 align-middle">{order.sku_id}</td>
                                        <td className="p-4 align-middle capitalize">
                                            <span className={`px-2 py-1 rounded-full text-xs ${order.status === 'routed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                                }`}>
                                                {order.status}
                                            </span>
                                        </td>
                                        <td className="p-4 align-middle">{order.fulfillment_node_id || '-'}</td>
                                        <td className="p-4 align-middle">
                                            {order.status === 'pending' && (
                                                <Button size="sm" onClick={() => routeOrder(order.id)}>Route</Button>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
