package org.cdi.advocacy.security;


public class SecurityService {
        
        private static ThreadLocal<SecurityToken> currentToken = new ThreadLocal<SecurityToken>();
        
        public static void placeSecurityToken(SecurityToken token){
                currentToken.set(token);
        }
        
        public void clearSecuirtyToken(){
                currentToken.set(null);
        }
        
        public boolean isLoggedIn(){
                SecurityToken token = currentToken.get();
                return token!=null;
        }
        
        public boolean isAllowed(String object, String method){
                SecurityToken token = currentToken.get();
                return token.isAllowed();
        }
        
        public String getCurrentUserName(){
                SecurityToken token = currentToken.get();
                if (token!=null){
                        return token.getUserName();
                }else {
                        return "Unknown";
                }
        }

}
