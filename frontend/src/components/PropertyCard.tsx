import React from 'react';
import { Link } from 'react-router-dom';
import { FiHeart, FiMapPin, FiDoor, FiSquare } from 'react-icons/fi';
import { Property } from '@/types';

interface PropertyCardProps {
  property: Property;
  onClick?: () => void;
}

const PropertyCard: React.FC<PropertyCardProps> = ({ property, onClick }) => {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: property.currency,
      notation: 'compact',
    }).format(price);
  };

  return (
    <Link
      to={`/properties/${property.id}`}
      className="card overflow-hidden hover:shadow-xl transition-all"
    >
      <div className="relative">
        <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
          <img
            src={`https://via.placeholder.com/400x300?text=${property.property_type}`}
            alt={property.title}
            className="w-full h-full object-cover"
          />
        </div>

        <div className="absolute top-3 right-3 bg-white rounded-full p-2 hover:bg-gray-100 cursor-pointer">
          <FiHeart size={20} />
        </div>

        {property.is_premium && (
          <div className="absolute top-3 left-3 badge badge-primary">Premium</div>
        )}
        {property.is_top && (
          <div className="absolute top-3 left-3 badge badge-success">Top</div>
        )}
      </div>

      <div className="p-4">
        <h3 className="text-lg font-bold text-gray-900 line-clamp-1">
          {property.title}
        </h3>

        <div className="flex items-center text-gray-600 text-sm mt-1">
          <FiMapPin size={16} className="mr-1" />
          <span>{property.district}, {property.region}</span>
        </div>

        <p className="text-2xl font-bold text-blue-600 mt-2">
          {formatPrice(property.price)}
        </p>

        <div className="flex gap-4 mt-3 text-sm text-gray-600 border-t pt-3">
          {property.rooms_count && (
            <div className="flex items-center">
              <FiDoor size={16} className="mr-1" />
              <span>{property.rooms_count} rooms</span>
            </div>
          )}
          <div className="flex items-center">
            <FiSquare size={16} className="mr-1" />
            <span>{property.square_meters} m²</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default PropertyCard;
