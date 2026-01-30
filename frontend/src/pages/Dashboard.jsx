import { useState, useEffect } from "react";
import Card from "../components/common/Card";
import { FiCalendar, FiUsers, FiAward, FiTrendingUp } from "react-icons/fi";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const StatCard = ({ icon: Icon, label, value, change }) => (
  <Card className="col-span-1">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-gray-400 text-sm mb-1">{label}</p>
        <p className="text-3xl font-bold text-white">{value}</p>
        <p
          className={`text-sm mt-2 ${change > 0 ? "text-green-400" : "text-red-400"}`}
        >
          {change > 0 ? "+" : ""}
          {change}% from last month
        </p>
      </div>
      <div className="bg-primary-600/20 p-4 rounded-lg">
        <Icon size={32} className="text-primary-500" />
      </div>
    </div>
  </Card>
);

export default function Dashboard() {
  const [stats] = useState({
    events: { value: 24, change: 12 },
    clubs: { value: 8, change: 5 },
    resources: { value: 45, change: 8 },
    attendees: { value: 320, change: 15 },
  });

  const [chartData] = useState([
    { name: "Jan", events: 4, clubs: 2, resources: 12 },
    { name: "Feb", events: 6, clubs: 3, resources: 15 },
    { name: "Mar", events: 8, clubs: 2, resources: 18 },
    { name: "Apr", events: 5, clubs: 4, resources: 20 },
    { name: "May", events: 9, clubs: 3, resources: 22 },
    { name: "Jun", events: 12, clubs: 5, resources: 25 },
  ]);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">Welcome back! Here's what's happening.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={FiCalendar}
          label="Events"
          value={stats.events.value}
          change={stats.events.change}
        />
        <StatCard
          icon={FiUsers}
          label="Clubs"
          value={stats.clubs.value}
          change={stats.clubs.change}
        />
        <StatCard
          icon={FiAward}
          label="Resources"
          value={stats.resources.value}
          change={stats.resources.change}
        />
        <StatCard
          icon={FiTrendingUp}
          label="Attendees"
          value={stats.attendees.value}
          change={stats.attendees.change}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Line Chart */}
        <Card>
          <h3 className="text-lg font-bold text-white mb-4">Activity Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1f2937",
                  border: "1px solid #374151",
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="events"
                stroke="#a855f7"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="clubs"
                stroke="#3b82f6"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Bar Chart */}
        <Card>
          <h3 className="text-lg font-bold text-white mb-4">
            Resource Utilization
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1f2937",
                  border: "1px solid #374151",
                }}
              />
              <Legend />
              <Bar dataKey="resources" fill="#a855f7" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Recent Events */}
      <Card>
        <h3 className="text-lg font-bold text-white mb-4">Recent Events</h3>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="flex items-center justify-between pb-4 border-b border-dark-700 last:border-0"
            >
              <div>
                <p className="font-medium text-white">
                  Tech Talk: AI in Education
                </p>
                <p className="text-sm text-gray-400">
                  March {15 + i}, 2024 • 2 PM
                </p>
              </div>
              <span className="badge badge-primary">Upcoming</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
