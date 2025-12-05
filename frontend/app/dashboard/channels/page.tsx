"use client"

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function ChannelsPage() {
    const [channels, setChannels] = useState<any[]>([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchChannels();
    }, []);

    const fetchChannels = async () => {
        try {
            const response = await api.get('/api/v1/fulfillment/channels');
            setChannels(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const createChannel = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        try {
            await api.post('/api/v1/fulfillment/channels', {
                name: formData.get('name'),
                type: formData.get('type'),
            });
            fetchChannels();
            setMessage('Channel created!');
        } catch (error) {
            console.error(error);
            setMessage('Failed to create channel.');
        }
    };

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Channel Management</h2>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Add Sales Channel</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={createChannel} className="space-y-4">
                            <Input name="name" placeholder="Channel Name (e.g. Shopify)" required />
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Type</label>
                                <select name="type" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                                    <option value="online">Online Store</option>
                                    <option value="marketplace">Marketplace</option>
                                    <option value="retail">Retail POS</option>
                                </select>
                            </div>
                            <Button type="submit">Add Channel</Button>
                        </form>
                        {message && <p className="text-sm text-green-600 mt-2">{message}</p>}
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Active Channels</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <ul className="space-y-2">
                            {channels.map((channel) => (
                                <li key={channel.id} className="p-3 border rounded-md flex justify-between items-center">
                                    <div>
                                        <p className="font-medium">{channel.name}</p>
                                        <p className="text-xs text-muted-foreground capitalize">{channel.type}</p>
                                    </div>
                                    <div className="text-xs bg-gray-100 p-1 rounded">
                                        API Key: {channel.api_key?.substring(0, 8)}...
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
