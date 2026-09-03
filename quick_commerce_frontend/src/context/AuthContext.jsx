import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(
    localStorage.getItem("accessToken")
  );

  const [refreshToken, setRefreshToken] = useState(
    localStorage.getItem("refreshToken")
  );

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user");

    return savedUser ? JSON.parse(savedUser) : null;
  });

  function login(authData) {
    const {
      access,
      refresh,
      user: authenticatedUser,
    } = authData;

    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    localStorage.setItem("user", JSON.stringify(authenticatedUser));

    setAccessToken(access);
    setRefreshToken(refresh);
    setUser(authenticatedUser);
  }

  function logout() {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");

    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
  }

  function updateAccessToken(token) {
  localStorage.setItem("accessToken", token);
  setAccessToken(token);
}

  const value = {
  accessToken,
  refreshToken,
  user,
  role: user?.role || null,
  isAuthenticated: Boolean(accessToken),
  login,
  logout,
  updateAccessToken,
};

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  return useContext(AuthContext);
}

export { AuthProvider, useAuth };