import type { MeInfo } from '@/api/users';
import { createContext, type ReactNode, useContext } from 'react';

export interface AuthContextValues {
  me: MeInfo | undefined;
  isLoading: boolean;
  isValidating: boolean;
}

const AuthContext = createContext<AuthContextValues>({ me: undefined, isLoading: false, isValidating: false, });

export function AuthProvider ({ children, ...context }: AuthContextValues & { children: ReactNode }) {
  return (
    <AuthContext.Provider value={context}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth () {
  return useContext(AuthContext);
}
