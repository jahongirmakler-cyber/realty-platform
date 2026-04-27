import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { propertyAPI } from '@/services/api';
import { PropertyDetail } from '@/types';
import { FiMapPin, FiDoor, FiSquare, FiPhone, FiMail } from 'react-icons/fi';
import toast from 'react-hot-toast';

const PropertyDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [property, setProperty] = useState<PropertyDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    loadProperty();
  }, [id]);

  const loadProperty = async () => {
    try {
      setLoading(true);
      const response = await propertyAPI.getById(parseInt(id!));
      setProperty(response.data);
    } catch (error) {
      toast.error('Failed to load property');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container py-8">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  if (!property) {
    return (
      <div className="container py-8">
        <div className="text-center text-gray-600">Property not found</div>
      </div>
    );
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: property.currency,
      notation: 'compact',
    }).format(price);
  };

  return (
    <div className="container py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Images */}
        <div className="lg:col-span-2">
          <div className="relative bg-gray-200 rounded-lg overflow-hidden h-96">
            <img
              src={`https://via.placeholder.com/800x600?text=${property.property_type}`}
              alt={property.title}
              className="w-full h-full object-cover"
            />
          </div>

          {/* Description */}
          <div className="mt-8 card p-6">
            <h1 className="text-3xl font-bold mb-4">{property.title}</h1>

            <div className="flex items-center text-gray-600 mb-4">
              <FiMapPin size={20} className="mr-2" />
              <span>{property.address}, {property.district}, {property.region}</span>
            </div>

            <p className="text-2xl font-bold text-blue-600 mb-4">
              {formatPrice(property.price)} / {property.listing_type}
            </p>

            <div className="grid grid-cols-3 gap-4 mb-6">
              {property.rooms_count && (
                <div className="text-center">
                  <FiDoor size={24} className="mx-auto mb-2" />
                  <p className="font-bold">{property.rooms_count}</p>
                  <p className="text-sm text-gray-600">Rooms</p>
                </div>
              )}
              <div className="text-center">
                <FiSquare size={24} className="mx-auto mb-2" />
                <p className="font-bold">{property.square_meters}</p>
                <p className="text-sm text-gray-600">m²</p>
              </div>
              {property.floor && (
                <div className="text-center">
                  <p className="font-bold text-2xl">{property.floor}/{property.total_floors}</p>
                  <p className="text-sm text-gray-600">Floor</p>
                </div>
              )}
            </div>

            <div className="border-t pt-6">
              <h2 className="text-xl font-bold mb-2">Description</h2>
              <p className="text-gray-600 leading-relaxed">
                {property.description || 'No description provided'}
              </p>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div>
          {/* Owner Card */}
          {property.owner && (
            <div className="card p-6 mb-6">
              <h3 className="font-bold text-lg mb-4">Agent Information</h3>

              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-gray-300 rounded-full"></div>
                <div>
                  <p className="font-bold">{property.owner.first_name} {property.owner.last_name}</p>
                  <p className="text-sm text-gray-600">@{property.owner.username}</p>
                </div>
              </div>

              <div className="space-y-2 mb-4">
                {property.owner.phone && (
                  <a
                    href={`tel:${property.owner.phone}`}
                    className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                  >
                    <FiPhone size={18} />
                    <span>{property.owner.phone}</span>
                  </a>
                )}
                <a
                  href={`mailto:${property.owner.email}`}
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                >
                  <FiMail size={18} />
                  <span>{property.owner.email}</span>
                </a>
              </div>

              <button className="btn-primary w-full">Contact Agent</button>
            </div>
          )}

          {/* Details Card */}
          <div className="card p-6">
            <h3 className="font-bold text-lg mb-4">Details</h3>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Property Type:</span>
                <span className="font-medium capitalize">{property.property_type}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Status:</span>
                <span className="font-medium capitalize">{property.property_status}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Views:</span>
                <span className="font-medium">{property.views_count}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Posted:</span>
                <span className="font-medium">{new Date(property.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyDetailPage;
