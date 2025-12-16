export type ISODateString = string;

export type UserRole = "admin" | "advisor" | "staff" | string;

// Shape returned by the Django REST profile serializer (snake_case field names).
export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  advisor_id: string | null;
  firm_name: string | null;
  role: UserRole;
  bio: string | null;
  avatar_url: string | null;
  date_joined: ISODateString;
}

// Allowed fields for PATCH /api/user/profile/.
export interface UserProfileUpdatePayload {
  first_name?: string;
  last_name?: string;
  bio?: string;
  avatar_url?: string;
}
