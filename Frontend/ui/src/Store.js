import React, { useState, useContext } from 'react'

const initialState = {
    authToken: "no-token",
    loggedIn: false
}
export const TokenContext = React.createContext();

const Store = ({ children }) => {
    const [globalAuthData, setGlobalAuthData] = useState(initialState);

    return (
        <TokenContext.Provider value={[globalAuthData, setGlobalAuthData]}>{children}</ TokenContext.Provider>
    )
};

export default Store