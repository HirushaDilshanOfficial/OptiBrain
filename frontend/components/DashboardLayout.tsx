"use client"

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { LayoutDashboard, TrendingUp, DollarSign, LogOut } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const { logout } = useAuth();

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <aside className="w-64 bg-white shadow-md">
                <div className="p-6">
                    <h1 className="text-2xl font-bold text-primary">OptiBrain</h1>
                </div>
                <nav className="mt-6">
                    <Link href="/dashboard" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <LayoutDashboard className="w-5 h-5 mr-3" />
                        Overview
                    </Link>
                    <Link href="/dashboard/sales" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <TrendingUp className="w-5 h-5 mr-3" />
                        Sales & Forecast
                    </Link>
                    <Link href="/dashboard/pricing" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <DollarSign className="w-5 h-5 mr-3" />
                        Dynamic Pricing
                    </Link>
                    <Link href="/dashboard/inventory" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <div className="w-5 h-5 mr-3 flex items-center justify-center">📦</div>
                        Inventory (AIR)
                    </Link>
                    <Link href="/dashboard/orders" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <div className="w-5 h-5 mr-3 flex items-center justify-center">📄</div>
                        Purchase Orders
                    </Link>
                    <Link href="/dashboard/fulfillment" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <div className="w-5 h-5 mr-3 flex items-center justify-center">🚚</div>
                        Fulfillment
                    </Link>
                    <Link href="/dashboard/channels" className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100">
                        <div className="w-5 h-5 mr-3 flex items-center justify-center">🌐</div>
                        Channels
                    </Link>
                </nav>
                <div className="absolute bottom-0 w-64 p-6">
                    <button onClick={logout} className="flex items-center text-red-500 hover:text-red-700">
                        <LogOut className="w-5 h-5 mr-3" />
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto p-8">
                {children}
            </main>
        </div>
    );
}
