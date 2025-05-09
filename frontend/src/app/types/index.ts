
export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: 'seeker' | 'provider' | 'admin'; 
    date_joined?: string;
  }
  
  export interface LoginCredentials {
    username: string; 
    password?: string;
  }
  
  export interface RegisterData extends LoginCredentials {
    email: string;
    first_name?: string;
    last_name?: string;
    role: 'seeker' | 'provider';
    password2: string;
  }
  
  export interface LoginResponse {
    access: string;  
    refresh: string; 
    user: User;      
  } 
  
  interface BaseProfileData {
    id: number;
    bio?: string;
    location?: string;
    created_at?: string; 
    updated_at?: string; 
    user: User; 
  }
  
  export interface SeekerProfileData extends BaseProfileData {
    industry_interest?: string;
    required_services?: string;
    project_description?: string;
    budget_range?: string;
  }
  
  export interface ProviderProfileData extends BaseProfileData {
    company_name?: string;
    services_offered?: string;
    experience_years?: number;
    portfolio_url?: string;
    industry_focus?: string;
    company_size?: string;
    rating_report_url?: string | null;
    hourly_rate?: string | number; 
  }

  export type UserProfile = SeekerProfileData | ProviderProfileData;  
  
  export type PartialSeekerProfileData = Partial<Omit<SeekerProfileData, 'id' | 'user' | 'created_at' | 'updated_at'>>;
  export type PartialProviderProfileData = Partial<Omit<ProviderProfileData, 'id' | 'user' | 'created_at' | 'updated_at'>>;
  
  export type PartialUserProfile = PartialSeekerProfileData | PartialProviderProfileData;