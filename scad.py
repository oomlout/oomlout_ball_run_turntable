import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)


radius_middle = 35 / 2
clearance_middle = 2/2/2

radius_ball = 8/2
clearance_ball = 1/2/2
lift_ball = 3

radius_motor_shaft = 3/2
clearance_motor_shaft = 0.5/2/2

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 5
        p3["height"] = 5
        p3["thickness"] = 9
        #p3["extra"] = ""
        part["kwargs"] = p3
        nam = "holder"
        part["name"] = nam
        if oomp_mode == "oobb":
            p3["oomp_size"] = nam
        parts.append(part)


        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 1
        p3["height"] = 1
        p3["thickness"] = 9 + 12
        #p3["extra"] = ""
        part["kwargs"] = p3
        nam = "shaft"
        part["name"] = nam
        if oomp_mode == "oobb":
            p3["oomp_size"] = nam
        parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    if True:
        #m6 holes
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = True  
        p3["radius_name"] = "m6"
        p3["depth"] = depth
        p3["holes"] = "single"
        locs = []
        locs.append([1,2])    
        locs.append([1,4])
        locs.append([2,5])
        locs.append([2,1])
        locs.append([4,1])
        locs.append([4,5])
        locs.append([5,2])
        locs.append([5,4])
        p3["locations"] = locs
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)
        #m3 holes
        p3 = copy.deepcopy(p3)
        p3["radius_name"] = "m3"
        locs = []
        locs.append([1,2.5])
        locs.append([1,3.5])
        locs.append([2.5,1])
        locs.append([2.5,5])
        locs.append([3.5,1])
        locs.append([3.5,5])
        locs.append([5,2.5])
        locs.append([5,3.5])
        p3["locations"] = locs
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    #motor mount
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_hole"
        p3["radius_name"] = "m3"
        p3["depth"] = depth
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        poss = []
        shift_x = 24.5
        shift_y = 0
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift_x
        pos11[1] += shift_y
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -shift_x
        pos12[1] += shift_y
        poss.append(pos12)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

    #middle_hole
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_hole"
        p3["radius"] = radius_middle + middle_clearance
        p3["depth"] = depth
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_holder(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    if True:
        #m6 holes
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = True  
        p3["radius_name"] = "m6"
        p3["depth"] = depth
        p3["holes"] = "single"
        locs = []
        locs.append([1,2])    
        locs.append([1,4])
        locs.append([2,5])
        locs.append([2,1])
        locs.append([4,1])
        locs.append([4,5])
        locs.append([5,2])
        locs.append([5,4])
        p3["locations"] = locs
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)
        #m3 holes
        p3 = copy.deepcopy(p3)
        p3["radius_name"] = "m3"
        locs = []
        locs.append([1,2.5])
        locs.append([1,3.5])
        locs.append([2.5,1])
        locs.append([2.5,5])
        locs.append([3.5,1])
        locs.append([3.5,5])
        locs.append([5,2.5])
        locs.append([5,3.5])
        p3["locations"] = locs
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    #motor mount
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["radius_name"] = "m3"
        p3["depth"] = depth
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[2] += depth
        poss = []
        shift_x = 22.211
        shift_y = 10.345
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift_x
        pos11[1] += -shift_y
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -shift_x
        pos12[1] += shift_y
        poss.append(pos12)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

    #middle_hole
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_hole"
        p3["radius"] = radius_middle + clearance_middle
        p3["depth"] = depth
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #ball runs
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = radius_ball + clearance_ball
        dep = 200
        p3["depth"] = dep
        rot1 = copy.deepcopy(rot)
        rot1[1] += 90
        p3["rot"] = rot1
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -dep/2
        pos1[1] += 0
        pos1[2] += dep/2 + depth/2 + lift_ball
        p3["pos"] = pos1
        p3["zz"] = "middle"
        
        p4 = copy.deepcopy(p3)
        oobb_base.append_full(thing,**p4)
        
        p4 = copy.deepcopy(p3)
        pos2 = copy.deepcopy(pos1)
        pos2[0] += dep/2
        pos2[1] += -dep/2
        pos2[2] += 0
        p4["pos"] = pos2
        rot2 = copy.deepcopy(rot1)
        rot2[2] += 90        
        p4["rot"] = rot2
        oobb_base.append_full(thing,**p4)


        p4 = copy.deepcopy(p3)
        pos2 = copy.deepcopy(pos1)
        pos2[0] += dep/4
        pos2[1] += -dep/4
        pos2[2] += 0
        p4["pos"] = pos2
        rot2 = copy.deepcopy(rot1)
        rot2[2] += 45
        p4["rot"] = rot2
        oobb_base.append_full(thing,**p4)

        p4 = copy.deepcopy(p3)
        pos2 = copy.deepcopy(pos1)
        pos2[0] += dep/4
        pos2[1] += dep/4
        pos2[2] += 0
        p4["pos"] = pos2
        rot2 = copy.deepcopy(rot1)
        rot2[2] += -45
        p4["rot"] = rot2
        oobb_base.append_full(thing,**p4)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_shaft(thing, **kwargs):

    motor_bump_depth = 2

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)   
    depth = depth - motor_bump_depth #for the bump                 
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    
    #add holes seperate
    if False:
        #m6 holes
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = True  
        p3["radius_name"] = "m6"
        p3["depth"] = depth
        p3["holes"] = "single"
        locs = []
        p3["locations"] = locs
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)
        #m3 holes
        p3 = copy.deepcopy(p3)
        p3["radius_name"] = "m3"
        locs = []
        p3["locations"] = locs
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    
    #middle_piece
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = radius_middle - clearance_middle
        p3["depth"] = depth
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[2] += depth/2
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #ball runs
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cylinder"
        p3["radius"] = radius_ball + clearance_ball
        dep = 200
        p3["depth"] = dep
        rot1 = copy.deepcopy(rot)
        rot1[1] += 90
        p3["rot"] = rot1
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -dep/2
        pos1[1] += 0
        pos1[2] += dep/2 + 9/2 + lift_ball + 12 - motor_bump_depth
        p3["pos"] = pos1
        p3["zz"] = "middle"
        
        p4 = copy.deepcopy(p3)
        oobb_base.append_full(thing,**p4)
        


    #add shaft
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_hole"
        p3["radius"] = radius_motor_shaft + clearance_motor_shaft
        p3["depth"] = 12
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[2] += 0
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add lock screw
    depth_shaft = 12
    depth_screw = 12
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["radius_name"] = "m3"
        p3["depth"] = depth_screw
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += depth_screw
        pos1[2] += depth_shaft/2
        p3["pos"] = pos1
        rot1 = copy.deepcopy(rot)
        rot1[1] += 90
        p3["rot"] = rot1
        p3["clearance"] = ["top"]
        oobb_base.append_full(thing,**p3)

        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_nut"
        p3["radius_name"] = "m3"
        #p3["depth"] = depth_screw
        p3["extra_clearance"] = 0.25
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += depth_screw / 2
        pos1[2] += depth_shaft/2
        p3["pos"] = pos1
        rot1 = copy.deepcopy(rot)
        rot1[1] += 90
        p3["rot"] = rot1
        p3["clearance"] = ["left"]
        oobb_base.append_full(thing,**p3)



        

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)