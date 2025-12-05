"use client"

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export default function AnalyticsPage() {
    const [salesData, setSalesData] = useState<any>(null);
    const [inventoryData, setInventoryData] = useState<any>(null);
    const [fulfillmentData, setFulfillmentData] = useState<any>(null);

    useEffect(() => {
        fetchAnalytics();
    }, []);

    const fetchAnalytics = async () => {
        try {
            const [salesRes, inventoryRes, fulfillmentRes] = await Promise.all([
                api.get('/api/v1/analytics/sales'),
                api.get('/api/v1/analytics/inventory'),
                api.get('/api/v1/analytics/fulfillment')
            ]);

            setSalesData(salesRes.data);
            setInventoryData(inventoryRes.data);
            setFulfillmentData(fulfillmentRes.data);
        } catch (error) {
            console.error("Failed to fetch analytics", error);
        }
    };

    if (!salesData || !inventoryData || !fulfillmentData) {
        return <div>Loading analytics...</div>;
    }

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Real-Time Analytics</h2>

            {/* KPI Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">${salesData.total_revenue.toLocaleString()}</div>
                        <p className="text-xs text-muted-foreground">+{salesData.revenue_growth}% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Units Sold</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{salesData.total_units_sold}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Low Stock Alerts</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-600">{inventoryData.low_stock_items}</div>
                        <p className="text-xs text-muted-foreground">Items below reorder point</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Avg Fulfillment Time</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{fulfillmentData.avg_fulfillment_time_hours}h</div>
                    </CardContent>
                </Card>
            </div>

            {/* Charts */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                    <CardHeader>
                        <CardTitle>Orders by Channel</CardTitle>
                    </CardHeader>
                    <CardContent className="pl-2">
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={fulfillmentData.orders_by_channel}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="count" fill="#8884d8" name="Orders" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                <Card className="col-span-3">
                    <CardHeader>
                        <CardTitle>Inventory Health</CardTitle>
                        <CardDescription>Stock status distribution</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[300px] w-full flex items-center justify-center">
                            {/* Mocking distribution for visualization since API returns aggregates */}
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={[
                                            { name: 'Healthy', value: inventoryData.total_sku_count - inventoryData.low_stock_items },
                                            { name: 'Low Stock', value: inventoryData.low_stock_items }
                                        ]}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {
                                            [
                                                { name: 'Healthy', value: inventoryData.total_sku_count - inventoryData.low_stock_items },
                                                { name: 'Low Stock', value: inventoryData.low_stock_items }
                                            ].map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={index === 1 ? '#ef4444' : '#22c55e'} />
                                            ))
                                        }
                                    </Pie>
                                    <Tooltip />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
