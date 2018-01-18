#Scott Dickson
#1/16/2018
#Converts audio samples to light output
#Light output is an array of 3-tuples

import numpy as np

class Light_Strip:
    def __init__(self,n,port=8080):
        self.spin_spots = []
        self.num_lights = n
        self.light_state = [Light() for i in range(n)]
        self.port = port
        #Consider layering each effect on the strip with differnet priorities
        
    #Basic method to set one of the pixels    
    def set_pixel(self,index,r,g,b):
        self.lights_state[index].color = [r,g,b]
        
        
    #Send the current rgb values of the light strip
    #through UDP on the target port.
    def send_config(self):
        pass
        
    #Follow the bass of the song. 
    def follow_bass(self):
        pass

    #Move a single color of LED in a circuit around the entire strip
    #of lights one light at a time for a spinning effect
    #0:red,1:green,2:blue
    #Spin spots is a tuple of the current index, color and starting index of
    #a light spin
    def start_spin(self,color, index):
        if index != 0:
            self.spin_spots += [[index,index-1,color]]
        else:
            self.spin_spots += [[index,self.num_lights - 1,color]]
    #For each spin spot update the light configuration
    def step_spin(self):
        new_spots = []
        
        #Clear colors of previous spin spots
        print(self.spin_spots)
        for l in self.spin_spots:
            self.light_state[l[0]].set_color(l[2],0)         
        
        #Add in new colors if necessary
        for l in self.spin_spots:
            #Check if we've reached our starting point. If so, terminate
            if l[0] != l[1]:           
                new_spots += [l]
                l[0] = l[0] + 1 if l[0] < self.num_lights - 1 else 0
                self.light_state[l[0]].set_color(l[2],255)
                self.light_state[l[0] - 1].set_color(l[2],0)
        self.spin_spots = new_spots    
        if new_spots == []:
            print('Finished spinning')
        
            
class Light:
    def __init__(self):
        #R,G,B
        self.color = [0,0,0]
    def __repr__(self):
        return '(' + str(self.color[0]) +','+str(self.color[1]) + ','+str(self.color[2]) + ')'
    def red(self):
        return self.color[0]
    def green(self):
        return self.color[1]
    def blue(self):
        return self.color[2]
    def set_color(self,color,v=0):
        self.color[color] = v

if __name__ == '__main__':
    
    n = 5
    l = Light_Strip(n)
    #print(l.spin_spots)
    print(l.num_lights)
    
    l.start_spin(0,1)
    for i in range(5):
        l.step_spin()
        print(l.light_state)
    
    
    
    
    
    