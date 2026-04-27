export interface User {
  id: number;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  avatar_url?: string;
  bio?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  is_premium: boolean;
  created_at: string;
}

export interface Property {
  id: number;
  owner_id: number;
  title: string;
  description?: string;
  property_type: string;
  property_status: string;
  region: string;
  district: string;
  address: string;
  rooms_count?: number;
  bathrooms_count?: number;
  square_meters: number;
  floor?: number;
  total_floors?: number;
  listing_type: string;
  price: number;
  currency: string;
  latitude?: number;
  longitude?: number;
  is_verified: boolean;
  is_premium: boolean;
  is_top: boolean;
  views_count: number;
  created_at: string;
  updated_at: string;
}

export interface PropertyImage {
  id: number;
  url: string;
  alt_text?: string;
  is_main: boolean;
}

export interface PropertyDetail extends Property {
  images: PropertyImage[];
  owner?: User;
}

export interface Listing {
  id: number;
  property_id: number;
  title: string;
  price: number;
  listing_type: string;
  is_active: boolean;
  is_premium: boolean;
  is_top: boolean;
  views_count: number;
  created_at: string;
}

export interface Agent {
  id: number;
  user_id: number;
  company_name?: string;
  license_number?: string;
  experience_years: number;
  is_premium: boolean;
  rating: float;
  total_properties: number;
  is_verified: boolean;
  created_at: string;
}
