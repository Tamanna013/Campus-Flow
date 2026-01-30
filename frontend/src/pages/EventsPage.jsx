import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Input from "../components/common/Input";
import {
  FiSearch,
  FiPlus,
  FiCalendar,
  FiMapPin,
  FiUsers,
} from "react-icons/fi";

const EventCard = ({ event }) => (
  <Card className="card-hover cursor-pointer">
    <div className="flex items-start gap-4">
      <img
        src={event.poster || "https://via.placeholder.com/100"}
        alt={event.title}
        className="w-20 h-20 rounded-lg object-cover"
      />
      <div className="flex-1">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-bold text-white hover:text-primary-500">
              {event.title}
            </h3>
            <p className="text-sm text-gray-400 mt-1">
              {event.description.substring(0, 100)}...
            </p>
          </div>
          <span
            className={`badge ${
              event.status === "upcoming"
                ? "badge-primary"
                : event.status === "ongoing"
                  ? "badge-success"
                  : "badge-warning"
            }`}
          >
            {event.status}
          </span>
        </div>

        <div className="flex items-center gap-4 mt-4 text-sm text-gray-400">
          <div className="flex items-center gap-1">
            <FiCalendar size={16} />
            {event.date}
          </div>
          <div className="flex items-center gap-1">
            <FiMapPin size={16} />
            {event.location}
          </div>
          <div className="flex items-center gap-1">
            <FiUsers size={16} />
            {event.attendees} attendees
          </div>
        </div>
      </div>
    </div>
  </Card>
);

export default function EventsPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");
  const [events, setEvents] = useState([
    {
      id: 1,
      title: "Tech Talk: AI in Education",
      description:
        "Join us for an exciting discussion about the role of AI in modern education.",
      date: "March 25, 2024",
      location: "Main Auditorium",
      attendees: 125,
      status: "upcoming",
      poster: "https://via.placeholder.com/100",
    },
    // Add more events...
  ]);

  const filteredEvents = events.filter((event) => {
    const matchesSearch = event.title
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesFilter =
      filterStatus === "all" || event.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white">Events</h1>
          <p className="text-gray-400 mt-1">
            Discover and manage campus events
          </p>
        </div>
        <Link to="/events/create">
          <Button variant="primary" size="lg">
            <FiPlus className="inline mr-2" />
            Create Event
          </Button>
        </Link>
      </div>

      {/* Filters */}
      <Card>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <FiSearch className="absolute left-3 top-3 text-gray-500" />
            <Input
              placeholder="Search events..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          <div>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="input-field"
            >
              <option value="all">All Events</option>
              <option value="upcoming">Upcoming</option>
              <option value="ongoing">Ongoing</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Events List */}
      <div className="space-y-4">
        {filteredEvents.length > 0 ? (
          filteredEvents.map((event) => (
            <Link key={event.id} to={`/events/${event.id}`}>
              <EventCard event={event} />
            </Link>
          ))
        ) : (
          <Card className="text-center py-12">
            <p className="text-gray-400">No events found</p>
          </Card>
        )}
      </div>
    </div>
  );
}
