import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { propertiesAPI } from '@/services/api';
import { Property } from '@/types';
import PropertyCard from '@/components/PropertyCard';
import FilterModal from '@/components/FilterModal';
import { FiFilter } from 'react-icons/fi';
import toast from 'react-hot-toast';

const PropertiesPage: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(20);
  const [filterOpen, setFilterOpen] = useState(false);
  const [filters, setFilters] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    loadProperties();
  }, [filters, skip]);

  const loadProperties = async () => {
    try {
      setLoading(true);
      let response;

      if (Object.keys(filters).length > 0) {
        response = await searchAPI.search({
          ...filters,
          skip,
          limit,
        });
        setProperties(response.data.results);
      } else {
        response = await propertiesAPI.getAll(skip, limit);
        setProperties(response.data);
      }
    } catch (error) {
      toast.error('Failed to load properties');
    } finally {
      setLoading(false);
    }
  };

  const handleApplyFilters = (newFilters: any) => {
    setFilters(newFilters);
    setSkip(0);
  };

  return (
    <div className="container py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Properties</h1>
        <button
          onClick={() => setFilterOpen(true)}
          className="btn-primary flex items-center gap-2"
        >
          <FiFilter size={20} />
          Filters
        </button>
      </div>

      <FilterModal
        isOpen={filterOpen}
        onClose={() => setFilterOpen(false)}
        onFilter={handleApplyFilters}
      />

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : properties.length === 0 ? (
        <div className="text-center py-8 text-gray-600">
          No properties found
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {properties.map((property) => (
              <PropertyCard key={property.id} property={property} />
            ))}
          </div>

          {/* Pagination */}
          <div className="flex justify-center gap-4">
            <button
              onClick={() => setSkip(Math.max(0, skip - limit))}
              disabled={skip === 0}
              className="btn-secondary"
            >
              Previous
            </button>
            <button
              onClick={() => setSkip(skip + limit)}
              className="btn-secondary"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default PropertiesPage;
