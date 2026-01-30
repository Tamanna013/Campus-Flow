import { useState } from "react";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import { FiCalendar, FiMapPin, FiUsers } from "react-icons/fi";
import { Calendar, ChevronRight } from "react-feather";

const ResourceCard = ({ resource }) => (
  <Card className="card-hover">
    <div className="flex items-start justify-between mb-4">
      <div>
        <h3 className="text-lg font-bold text-white">{resource.name}</h3>
        <p className="text-sm text-gray-400">{resource.type}</p>
      </div>
      <span
        className={`badge ${resource.available ? "badge-success" : "badge-error"}`}
      >
        {resource.available ? "Available" : "Booked"}
      </span>
    </div>

    <p className="text-sm text-gray-300 mb-4">{resource.description}</p>

    <div className="space-y-2 mb-4 text-sm text-gray-400">
      <div className="flex items-center gap-2">
        <FiMapPin size={16} />
        {resource.location}
      </div>
      {resource.capacity && (
        <div className="flex items-center gap-2">
          <FiUsers size={16} />
          Capacity: {resource.capacity}
        </div>
      )}
    </div>

    <Button variant="outline" size="sm" className="w-full">
      <Calendar size={16} className="mr-2" />
      Book Now
    </Button>
  </Card>
);

export default function ResourcesPage() {
  const [resources] = useState([
    {
      id: 1,
      name: "Main Auditorium",
      type: "Hall",
      description:
        "Large auditorium perfect for conferences and large meetings.",
      location: "Building A, Ground Floor",
      capacity: 500,
      available: true,
    },
    // Add more resources...
  ]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-white">Resources</h1>
        <p className="text-gray-400 mt-1">Browse and book campus resources</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((resource) => (
          <ResourceCard key={resource.id} resource={resource} />
        ))}
      </div>
    </div>
  );
}
