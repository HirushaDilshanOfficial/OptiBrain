"use client"

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function CustomersPage() {
    const [customers, setCustomers] = useState<any[]>([]);
    const [segments, setSegments] = useState<any[]>([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchCustomers();
        fetchSegments();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await api.get('/api/v1/customers/');
            setCustomers(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchSegments = async () => {
        try {
            const response = await api.get('/api/v1/customers/segments');
            setSegments(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const createCustomer = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        try {
            await api.post('/api/v1/customers/', {
                full_name: formData.get('name'),
                email: formData.get('email'),
                phone_number: formData.get('phone'),
            });
            fetchCustomers();
            setMessage('Customer created!');
            (e.target as HTMLFormElement).reset();
        } catch (error) {
            console.error(error);
            setMessage('Failed to create customer.');
        }
    };

    const triggerSegmentation = async () => {
        try {
            await api.post('/api/v1/customers/segment', {});
            setMessage('Segmentation complete!');
            fetchCustomers();
            fetchSegments();
        } catch (error) {
            console.error(error);
            setMessage('Segmentation failed.');
        }
    };

    const getSegmentName = (segmentId: number | null) => {
        if (segmentId === null) return 'Not Segmented';
        const segment = segments.find(s => s.id === segmentId);
        return segment ? segment.name : 'Unknown';
    };

    const getSegmentColor = (segmentId: number | null) => {
        if (segmentId === null) return 'bg-gray-100 text-gray-800';
        if (segmentId === 0) return 'bg-red-100 text-red-800';
        if (segmentId === 1) return 'bg-yellow-100 text-yellow-800';
        return 'bg-green-100 text-green-800';
    };

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Customer Management</h2>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Add New Customer</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={createCustomer} className="space-y-4">
                            <Input name="name" placeholder="Full Name" required />
                            <Input name="email" placeholder="Email" type="email" required />
                            <Input name="phone" placeholder="Phone Number" />
                            <Button type="submit">Add Customer</Button>
                        </form>
                        {message && <p className="text-sm text-green-600 mt-2">{message}</p>}
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>AI Segmentation</CardTitle>
                        <CardDescription>Group customers by purchasing behavior</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Button onClick={triggerSegmentation} variant="secondary" className="w-full">
                            Run Segmentation (K-Means)
                        </Button>
                        <div className="text-sm">
                            <p><strong>Segments:</strong></p>
                            <ul className="list-disc pl-5 mt-2">
                                {segments.map(seg => (
                                    <li key={seg.id}>{seg.name}: {seg.description}</li>
                                ))}
                            </ul>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Customer List</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="relative w-full overflow-auto">
                        <table className="w-full caption-bottom text-sm">
                            <thead className="[&_tr]:border-b">
                                <tr className="border-b transition-colors hover:bg-muted/50">
                                    <th className="h-12 px-4 text-left align-middle font-medium">ID</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium">Name</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium">Email</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium">Segment</th>
                                </tr>
                            </thead>
                            <tbody>
                                {customers.map((customer) => (
                                    <tr key={customer.id} className="border-b transition-colors hover:bg-muted/50">
                                        <td className="p-4 align-middle">{customer.id}</td>
                                        <td className="p-4 align-middle">{customer.full_name || '-'}</td>
                                        <td className="p-4 align-middle">{customer.email}</td>
                                        <td className="p-4 align-middle">
                                            <span className={`px-2 py-1 rounded-full text-xs ${getSegmentColor(customer.segment_id)}`}>
                                                {getSegmentName(customer.segment_id)}
                                            </span>
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
