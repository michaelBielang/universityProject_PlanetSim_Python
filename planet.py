class planet:

    def __init__(self, mass, name, pos_x, pos_y, pos_z, v_x, v_y, v_z):
        self.mass = mass
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.v_x = v_x
        self.v_z = v_z
        self.v_y = v_y

    def get_position(self):
        return [self.pos_x, self.pos_y, self.pos_z]

    def get_velocity(self):
        return [self.v_x, self.v_y, self.v_z]

    def set_position(self, new_x, new_y, new_z):
        self.pos_x = new_x
        self.pos_y = new_y
        self.pos_z = new_z

    def set_velocity(self, new_v_x, new_v_y, new_v_z):
        self.v_x = new_v_x
        self.v_z = new_v_y
        self.v_y = new_v_z

    def get_mass(self):
        return self.mass
