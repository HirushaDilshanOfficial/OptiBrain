"use client"

import React, { useState } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function PricingPage() {
    const [skuId, setSkuId] = useState('');
    const [minPrice, setMinPrice] = useState('');
    const [maxPrice, setMaxPrice] = useState('');
    const [currentPrice, setCurrentPrice] = useState('');
    const [inventory, setInventory] = useState('');
    const [optimizationResult, setOptimizationResult] = useState<any>(null);
    const [message, setMessage] = useState('');

    const createRule = async () => {
        try {
            await api.post('/api/v1/pricing/rules', {
                sku_id: skuId,
                min_price: parseFloat(minPrice),
                max_price: parseFloat(maxPrice),
            });
            setMessage('Rule created successfully!');
        } catch (error) {
            console.error(error);
            setMessage('Failed to create rule.');
        }
    };

    const optimizePrice = async () => {
        try {
            const response = await api.post('/api/v1/pricing/optimize', {
                sku_id: skuId,
                current_price: parseFloat(currentPrice),
                inventory_level: parseInt(inventory),
            });
            setOptimizationResult(response.data);
        } catch (error) {
            console.error(error);
            setMessage('Optimization failed.');
        }
    };

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Dynamic Pricing Manager</h2>

            <div className="grid gap-6 md:grid-cols-2">
                {/* Create Rule Section */}
                <Card>
                    <CardHeader>
                        <CardTitle>Set Pricing Rules</CardTitle>
                        <CardDescription>Define guardrails for your dynamic pricing engine.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">SKU ID</label>
                            <Input value={skuId} onChange={(e) => setSkuId(e.target.value)} placeholder="e.g., item_1" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Min Price ($)</label>
                                <Input type="number" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} placeholder="10.00" />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Max Price ($)</label>
                                <Input type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} placeholder="50.00" />
                            </div>
                        </div>
                        <Button onClick={createRule} className="w-full">Save Rule</Button>
                        {message && <p className="text-sm text-green-600">{message}</p>}
                    </CardContent>
                </Card>

                {/* Optimize Section */}
                <Card>
                    <CardHeader>
                        <CardTitle>Trigger Optimization</CardTitle>
                        <CardDescription>Manually trigger the pricing engine for a SKU.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Current Price ($)</label>
                            <Input type="number" value={currentPrice} onChange={(e) => setCurrentPrice(e.target.value)} placeholder="25.00" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Inventory Level</label>
                            <Input type="number" value={inventory} onChange={(e) => setInventory(e.target.value)} placeholder="100" />
                        </div>
                        <Button onClick={optimizePrice} variant="secondary" className="w-full">Optimize Price</Button>

                        {optimizationResult && (
                            <div className="mt-4 p-4 bg-gray-50 rounded-md border">
                                <h4 className="font-semibold mb-2">Optimization Result</h4>
                                <div className="grid grid-cols-2 gap-2 text-sm">
                                    <span className="text-gray-500">New Price:</span>
                                    <span className="font-bold text-green-600">${optimizationResult.new_price.toFixed(2)}</span>
                                    <span className="text-gray-500">Reason:</span>
                                    <span>{optimizationResult.reason}</span>
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
