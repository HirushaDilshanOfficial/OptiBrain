"use client"

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function InventoryPage() {
    const [suppliers, setSuppliers] = useState<any[]>([]);
    const [skuId, setSkuId] = useState('');
    const [outletId, setOutletId] = useState('store_1');
    const [replenishmentResult, setReplenishmentResult] = useState<any>(null);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchSuppliers();
    }, []);

    const fetchSuppliers = async () => {
        try {
            const response = await api.get('/api/v1/inventory/suppliers');
            setSuppliers(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const createSupplier = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        try {
            await api.post('/api/v1/inventory/suppliers', {
                name: formData.get('name'),
                lead_time_days: parseInt(formData.get('lead_time') as string),
                contact_email: formData.get('email'),
            });
            fetchSuppliers();
            setMessage('Supplier added!');
        } catch (error) {
            console.error(error);
            setMessage('Failed to add supplier.');
        }
    };

    const triggerReplenishment = async () => {
        try {
            const response = await api.post('/api/v1/inventory/replenish', {
                sku_id: skuId,
                outlet_id: outletId,
            });
            setReplenishmentResult(response.data);
            setMessage('Replenishment triggered!');
        } catch (error: any) {
            console.error(error);
            if (error.response?.status === 200) {
                setMessage(error.response.data.detail);
                setReplenishmentResult(null);
            } else {
                setMessage('Replenishment failed.');
            }
        }
    };

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Inventory & Replenishment</h2>

            <div className="grid gap-6 md:grid-cols-2">
                {/* Supplier Management */}
                <Card>
                    <CardHeader>
                        <CardTitle>Add Supplier</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={createSupplier} className="space-y-4">
                            <Input name="name" placeholder="Supplier Name" required />
                            <Input name="email" placeholder="Contact Email" type="email" />
                            <Input name="lead_time" placeholder="Lead Time (Days)" type="number" required />
                            <Button type="submit">Add Supplier</Button>
                        </form>
                        <div className="mt-4">
                            <h4 className="font-semibold mb-2">Existing Suppliers</h4>
                            <ul className="list-disc pl-5 text-sm">
                                {suppliers.map((s) => (
                                    <li key={s.id}>{s.name} ({s.lead_time_days} days)</li>
                                ))}
                            </ul>
                        </div>
                    </CardContent>
                </Card>

                {/* Replenishment Trigger */}
                <Card>
                    <CardHeader>
                        <CardTitle>Trigger Replenishment (AIR)</CardTitle>
                        <CardDescription>Calculate reorder points and generate POs.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Input value={skuId} onChange={(e) => setSkuId(e.target.value)} placeholder="SKU ID" />
                        <Input value={outletId} onChange={(e) => setOutletId(e.target.value)} placeholder="Outlet ID" />
                        <Button onClick={triggerReplenishment} variant="secondary">Run AIR</Button>

                        {message && <p className="text-sm mt-2">{message}</p>}

                        {replenishmentResult && (
                            <div className="mt-4 p-4 bg-green-50 rounded-md border border-green-200">
                                <h4 className="font-semibold text-green-800 mb-2">Purchase Order Generated!</h4>
                                <div className="text-sm text-green-700">
                                    <p>PO ID: {replenishmentResult.id}</p>
                                    <p>Quantity: {replenishmentResult.quantity}</p>
                                    <p>Status: {replenishmentResult.status}</p>
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
