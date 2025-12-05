"use client"

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function SalesPage() {
    const [skuId, setSkuId] = useState('item_1');
    const [forecastData, setForecastData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchForecast = async () => {
        setLoading(true);
        try {
            // In a real app, we might fetch history + forecast separately or combined
            // For now, let's assume the forecast endpoint returns the structure we need
            // or we simulate it.

            // Fetching forecast from our API
            const response = await api.get(`/api/v1/sales/forecast/${skuId}?days=7`);

            // The API returns a single forecast object for the latest timestamp in our current implementation
            // To make the chart interesting, let's mock a series of data points if the API doesn't return a list yet.
            // Ideally, the API should return a list of historical + forecast points.

            // MOCKING DATA FOR VISUALIZATION PURPOSES UNTIL API RETURNS LIST
            const mockData = [
                { date: '2023-10-20', sales: 120, forecast: null },
                { date: '2023-10-21', sales: 132, forecast: null },
                { date: '2023-10-22', sales: 101, forecast: null },
                { date: '2023-10-23', sales: 134, forecast: null },
                { date: '2023-10-24', sales: 90, forecast: null },
                { date: '2023-10-25', sales: 230, forecast: null },
                { date: '2023-10-26', sales: null, forecast: response.data.predicted_quantity },
                { date: '2023-10-27', sales: null, forecast: response.data.predicted_quantity * 1.1 },
                { date: '2023-10-28', sales: null, forecast: response.data.predicted_quantity * 0.9 },
            ];

            setForecastData(mockData);
        } catch (error) {
            console.error("Failed to fetch forecast", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Sales & Forecast</h2>

            <Card>
                <CardHeader>
                    <CardTitle>Demand Forecast</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex space-x-4 mb-6">
                        <Input
                            placeholder="SKU ID"
                            value={skuId}
                            onChange={(e) => setSkuId(e.target.value)}
                            className="w-[200px]"
                        />
                        <Button onClick={fetchForecast} disabled={loading}>
                            {loading ? 'Loading...' : 'Generate Forecast'}
                        </Button>
                    </div>

                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={forecastData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="sales" stroke="#8884d8" name="Actual Sales" />
                                <Line type="monotone" dataKey="forecast" stroke="#82ca9d" name="Forecast" strokeDasharray="5 5" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
