import React, { useState } from 'react';
import { FiSearch, FiFilter } from 'react-icons/fi';
import { searchAPI } from '@/services/api';
import toast from 'react-hot-toast';

interface FilterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onFilter: (filters: any) => void;
}

const FilterModal: React.FC<FilterModalProps> = ({ isOpen, onClose, onFilter }) => {
  const [filters, setFilters] = useState({
    property_type: '',
    region: '',
    district: '',
    min_price: '',
    max_price: '',
    min_rooms: '',
    max_rooms: '',
    listing_type: '',
  });

  const [regions, setRegions] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);

  React.useEffect(() => {
    if (isOpen) {
      loadRegions();
    }
  }, [isOpen]);

  const loadRegions = async () => {
    try {
      const response = await searchAPI.getRegions();
      setRegions(response.data.regions);
    } catch (error) {
      toast.error('Failed to load regions');
    }
  };

  const handleRegionChange = async (region: string) => {
    setFilters({ ...filters, region, district: '' });
    if (region) {
      try {
        const response = await searchAPI.getDistricts(region);
        setDistricts(response.data.districts);
      } catch (error) {
        toast.error('Failed to load districts');
      }
    }
  };

  const handleApplyFilters = () => {
    onFilter(filters);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold mb-4">Filters</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Property Type</label>
            <select
              value={filters.property_type}
              onChange={(e) => setFilters({ ...filters, property_type: e.target.value })}
              className="input-field"
            >
              <option value="">All Types</option>
              <option value="apartment">Apartment</option>
              <option value="house">House</option>
              <option value="land">Land</option>
              <option value="commercial">Commercial</option>
              <option value="office">Office</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Listing Type</label>
            <select
              value={filters.listing_type}
              onChange={(e) => setFilters({ ...filters, listing_type: e.target.value })}
              className="input-field"
            >
              <option value="">All Types</option>
              <option value="sale">Sale</option>
              <option value="rent">Rent</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Region</label>
            <select
              value={filters.region}
              onChange={(e) => handleRegionChange(e.target.value)}
              className="input-field"
            >
              <option value="">Select Region</option>
              {regions.map((region) => (
                <option key={region} value={region}>
                  {region}
                </option>
              ))}
            </select>
          </div>

          {filters.region && (
            <div>
              <label className="block text-sm font-medium mb-2">District</label>
              <select
                value={filters.district}
                onChange={(e) => setFilters({ ...filters, district: e.target.value })}
                className="input-field"
              >
                <option value="">Select District</option>
                {districts.map((district) => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Min Price</label>
              <input
                type="number"
                value={filters.min_price}
                onChange={(e) => setFilters({ ...filters, min_price: e.target.value })}
                placeholder="Min"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Max Price</label>
              <input
                type="number"
                value={filters.max_price}
                onChange={(e) => setFilters({ ...filters, max_price: e.target.value })}
                placeholder="Max"
                className="input-field"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Min Rooms</label>
              <input
                type="number"
                value={filters.min_rooms}
                onChange={(e) => setFilters({ ...filters, min_rooms: e.target.value })}
                placeholder="Min"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Max Rooms</label>
              <input
                type="number"
                value={filters.max_rooms}
                onChange={(e) => setFilters({ ...filters, max_rooms: e.target.value })}
                placeholder="Max"
                className="input-field"
              />
            </div>
          </div>
        </div>

        <div className="flex gap-4 mt-6">
          <button
            onClick={onClose}
            className="btn-secondary flex-1"
          >
            Close
          </button>
          <button
            onClick={handleApplyFilters}
            className="btn-primary flex-1"
          >
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilterModal;
