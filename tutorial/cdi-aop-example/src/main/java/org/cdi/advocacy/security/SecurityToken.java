package org.cdi.advocacy.security;

/**
 * @author Richard Hightower
 *
 */
public class SecurityToken {
        
        private boolean allowed;
        private String userName;
        
        public SecurityToken() {
                
        }
        
        
        
        public SecurityToken(boolean allowed, String userName) {
                super();
                this.allowed = allowed;
                this.userName = userName;
        }



        public boolean isAllowed(String object, String methodName) {
                return allowed;
        }

        
        /**
         * @return Returns the allowed.
         */
        public boolean isAllowed() {
                return allowed;
        }
        /**
         * @param allowed The allowed to set.
         */
        public void setAllowed(boolean allowed) {
                this.allowed = allowed;
        }
        /**
         * @return Returns the userName.
         */
        public String getUserName() {
                return userName;
        }
        /**
         * @param userName The userName to set.
         */
        public void setUserName(String userName) {
                this.userName = userName;
        }
}