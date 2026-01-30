import { useState } from "react";
import { Link } from "react-router-dom";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import { FiPlus, FiUsers, FiCalendar } from "react-icons/fi";

const ClubCard = ({ club }) => (
  <Card className="card-hover hover:shadow-lg hover:shadow-primary-900/30">
    <div className="flex items-start gap-4">
      <img
        src={club.logo || "https://via.placeholder.com/80"}
        alt={club.name}
        className="w-20 h-20 rounded-lg object-cover"
      />
      <div className="flex-1">
        <h3 className="text-lg font-bold text-white">{club.name}</h3>
        <p className="text-sm text-gray-400 mb-2">{club.category}</p>
        <p className="text-sm text-gray-300 mb-3">
          {club.description.substring(0, 100)}...
        </p>

        <div className="flex items-center gap-4 text-sm text-gray-400">
          <div className="flex items-center gap-1">
            <FiUsers size={16} />
            {club.members} members
          </div>
          <div className="flex items-center gap-1">
            <FiCalendar size={16} />
            {club.events} events
          </div>
        </div>
      </div>
    </div>
  </Card>
);

export default function ClubsPage() {
  const [clubs] = useState([
    {
      id: 1,
      name: "AI & Machine Learning Club",
      category: "Technical",
      description:
        "Explore the world of artificial intelligence and machine learning with fellow enthusiasts.",
      logo: "https://via.placeholder.com/80",
      members: 45,
      events: 12,
    },
    // Add more clubs...
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white">Clubs</h1>
          <p className="text-gray-400 mt-1">
            Join clubs and grow your community
          </p>
        </div>
        <Button variant="primary" size="lg">
          <FiPlus className="inline mr-2" />
          Create Club
        </Button>
      </div>

      {/* Clubs Grid */}
      <div className="grid grid-cols-1 gap-4">
        {clubs.map((club) => (
          <Link key={club.id} to={`/clubs/${club.id}`}>
            <ClubCard club={club} />
          </Link>
        ))}
      </div>
    </div>
  );
}
