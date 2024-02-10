import numpy as np

class Actor():
    def __init__(self, alpha):
        self.alpha = alpha
        angles = np.array([i*np.pi/4 for i in range(8)]).reshape(8,1)
        self.theta = np.hstack((55*np.ones((8,1)), 200/(512*np.sqrt(2))*np.ones((8,1)), np.zeros((8,1)), angles, 10*np.ones((8,1))))
    
    def __call__(self, s):
        e = np.array([s['desired_position'][0]-s['current_position'][0], s['current_position'][1]-s['desired_position'][1]])
        abs_e = np.linalg.norm(e)
        ang_e = (np.arctan2(e[1],e[0]) + 2*np.pi) % 2*np.pi
        
        mean = (self.theta[:,0] + self.theta[:,1]*abs_e + self.theta[:,2]*abs_e**2) * (np.exp(-(ang_e - self.theta[:,3])**2))
        cov = np.eye(8,8) / np.exp(self.theta[:,3])**2
        action = np.random.default_rng().multivariate_normal(mean, cov)
        
        return np.clip(action, 0, 255).astype(int)
        
    
    def update(self, I, delta, state, action):
        self.theta += self.alpha * I * delta * self.grad_ln(state, action)
    
    def grad_ln(self, s, a):
        e = np.array([s['desired_position'][0]-s['current_position'][0], s['current_position'][1]-s['desired_position'][1]])
        abs_e = np.linalg.norm(e)
        ang_e = (np.arctan2(e[1],e[0]) + 2*np.pi) % 2*np.pi
        M = np.zeros((8,5))
        
        mu = self.theta[:,0] + self.theta[:,1]*abs_e + self.theta[:,2]*abs_e**2
        k = np.exp(-(ang_e - self.theta[:,3])**2)
        
        M[:,0] = k * (a-mu*k) * np.exp(2*self.theta[:,4])
        M[:,1] = abs_e * M[:,0]
        M[:,2] = abs_e**2 * M[:,0]
        M[:,3] = 2 * (ang_e - self.theta[:,3]) * mu * M[:,0]
        M[:,4] = 1 - np.exp(2*self.theta[:,4]) * (a-mu*k)**2
        
        return M


class Critic:
    def __init__(self, alpha):
        self.w = np.zeros(4)
        self.alpha = alpha
    
    def value(self, state):
        abs_e = self._calc_error(state)
        return self.w[0] + self.w[1]*abs_e + self.w[2]*abs_e**2 + self.w[3]*abs_e**3
    
    def update(self, delta, state):
        abs_e = self._calc_error(state)
        self.w += self.alpha * delta * np.array([1, abs_e, abs_e**2, abs_e**3])
        
    def _calc_error(self, s):
        e = np.array([s['desired_position'][0]-s['current_position'][0], s['current_position'][1]-s['desired_position'][1]])
        return np.linalg.norm(e)