# Ryuo GLB generator for Blender 4.x
# Usage: blender --background --python tools/create_ryuo.py
# Output: assets/fighters/ryuo.glb
import bpy, math, os
from mathutils import Vector

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "fighters", "ryuo.glb"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.armatures, bpy.data.actions, bpy.data.materials):
    pass

def mat(name, color, metallic=0.0, rough=.42, emission=0.0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF"); p.inputs["Base Color"].default_value=(*color,1)
    p.inputs["Metallic"].default_value=metallic; p.inputs["Roughness"].default_value=rough
    if emission:
        p.inputs["Emission Color"].default_value=(*color,1); p.inputs["Emission Strength"].default_value=emission
    return m
navy=mat("Ryuo | Midnight Fabric",(0.018,.045,.11),.2,.34)
blue=mat("Ryuo | Cobalt Armor",(.015,.12,.48),.48,.27,.18)
cyan=mat("Ryuo | Energy Cyan",(.01,.55,1),.35,.22,2.2)
skin=mat("Ryuo | Warm Skin",(.62,.34,.23),0,.48)
hair=mat("Ryuo | Obsidian Hair",(.012,.018,.045),.12,.3)
white=mat("Ryuo | Eye Highlights",(.7,.92,1),.05,.2,1.1)
sole=mat("Ryuo | Boot Soles",(.025,.04,.075),.25,.4)

# Humanoid skeleton, facing +Y (front); character height about 2.5m.
bpy.ops.object.armature_add(enter_editmode=True, location=(0,0,0))
arm=bpy.context.object; arm.name="Ryuo_Rig"; arm.data.name="Ryuo_Skeleton"
eb=arm.data.edit_bones; eb.remove(eb[0])
bones=[
("root",(0,0,.08),(0,0,.25),None),
("hips",(0,0,.9),(0,0,1.12),"root"),
("spine",(0,0,1.05),(0,0,1.48),"hips"),
("chest",(0,0,1.42),(0,0,1.72),"spine"),
("neck",(0,0,1.68),(0,0,1.83),"chest"),
("head",(0,0,1.8),(0,0,2.13),"neck"),
("upper_arm.L",(.22,0,1.63),(.48,0,1.4),"chest"),
("forearm.L",(.48,0,1.4),(.55,.02,1.17),"upper_arm.L"),
("hand.L",(.55,.02,1.17),(.57,.06,1.08),"forearm.L"),
("upper_arm.R",(-.22,0,1.63),(-.48,0,1.4),"chest"),
("forearm.R",(-.48,0,1.4),(-.55,.02,1.17),"upper_arm.R"),
("hand.R",(-.55,.02,1.17),(-.57,.06,1.08),"forearm.R"),
("thigh.L",(.13,0,.98),(.16,0,.57),"hips"),
("shin.L",(.16,0,.57),(.16,.02,.17),"thigh.L"),
("foot.L",(.16,0,.17),(.16,.18,.1),"shin.L"),
("thigh.R",(-.13,0,.98),(-.16,0,.57),"hips"),
("shin.R",(-.16,0,.57),(-.16,.02,.17),"thigh.R"),
("foot.R",(-.16,0,.17),(-.16,.18,.1),"shin.R"),
]
for name,head,tail,parent in bones:
 b=eb.new(name); b.head=head; b.tail=tail
 if parent: b.parent=eb.get(parent)
bpy.ops.object.mode_set(mode="OBJECT")
arm.show_in_front=True
arm.data.display_type="STICK"

parts=[]
def uv(name, loc, scale, material, bone, segments=16):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=12, location=loc)
 o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
 o.data.materials.append(material); parts.append((o,bone)); return o
def cube(name, loc, scale, material, bone, bevel=.04):
 bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale
 bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(material)
 if bevel:
  mod=o.modifiers.new("Soft armor edges","BEVEL"); mod.width=bevel; mod.segments=2
  o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
 parts.append((o,bone)); return o
def cone(name, loc, radius, depth, material, bone, rot=(0,0,0)):
 bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=radius, radius2=0, depth=depth, location=loc, rotation=rot)
 o=bpy.context.object; o.name=name; o.data.materials.append(material); parts.append((o,bone)); return o

# Core body, layered outfit and head.
uv("Torso undersuit",(0,0,1.48),(.31,.19,.39),navy,"chest")
uv("Chest armor",(0,.018,1.55),(.34,.205,.22),blue,"chest")
cube("Cyan chest crest",(0,.222,1.55),(.075,.018,.14),cyan,"chest",.015)
uv("Belt",(0,0,1.13),(.31,.205,.085),blue,"hips")
cube("Belt buckle",(0,.211,1.14),(.1,.025,.09),cyan,"hips",.015)
uv("Neck",(0,0,1.79),(.105,.1,.12),skin,"neck")
uv("Face",(0,.008,1.94),(.19,.17,.235),skin,"head")
uv("Hair cap",(0,-.018,2.08),(.205,.18,.15),hair,"head")
for i in range(7):
 x=(i-3)*.052
 cone("Hair spike %02d"%i,(x,-.005,2.19-abs(i-2)*.012),.075,.24,hair,"head",(0,(-.2+i*.055),0))
# eyes face toward +Y
for x in (-.075,.075):
 cube("Glowing eye",(x,.165,1.98),(.055,.018,.018),white,"head",.008)
 cube("Blue eye edge",(x,.178,1.98),(.058,.008,.008),cyan,"head",.003)
# scarf tails
for s in (-1,1):
 tail=cube("Scarf tail",(s*.22,-.18,1.42),(.13,.07,.48),blue,"chest",.035); tail.rotation_euler[1]=s*.18
# limbs are deliberately segmented to keep stylized silhouette readable.
for s,side in ((1,"L"),(-1,"R")):
 uv("Shoulder "+side,(s*.34,0,1.62),(.17,.17,.17),blue,"chest")
 uv("Upper arm "+side,(s*.43,0,1.43),(.12,.13,.22),skin,"upper_arm."+side)
 uv("Arm guard "+side,(s*.47,.01,1.38),(.135,.145,.13),blue,"upper_arm."+side)
 uv("Forearm "+side,(s*.53,.015,1.22),(.105,.11,.19),skin,"forearm."+side)
 uv("Energy bracer "+side,(s*.54,.045,1.22),(.12,.12,.15),cyan,"forearm."+side)
 uv("Fist "+side,(s*.56,.05,1.09),(.105,.1,.095),skin,"hand."+side)
 uv("Thigh "+side,(s*.15,0,.78),(.145,.15,.26),navy,"thigh."+side)
 uv("Knee guard "+side,(s*.16,.12,.58),(.13,.06,.105),blue,"shin."+side)
 uv("Shin "+side,(s*.16,0,.38),(.105,.115,.23),navy,"shin."+side)
 cube("Boot "+side,(s*.16,.075,.16),(.23,.34,.16),blue,"foot."+side,.04)
 cube("Boot sole "+side,(s*.16,.1,.085),(.24,.37,.045),sole,"foot."+side,.015)
 cube("Boot trim "+side,(s*.16,.252,.17),(.18,.018,.035),cyan,"foot."+side,.008)

# Join all mesh parts into one skinned mesh, assigning each part to its corresponding bone.
bpy.ops.object.select_all(action="DESELECT")
for o,bn in parts: o.select_set(True)
bpy.context.view_layer.objects.active=parts[0][0]
bpy.ops.object.join()
mesh=bpy.context.object; mesh.name="Ryuo_Mesh"
for bn in arm.data.bones:
 mesh.vertex_groups.new(name=bn.name)
# Each primitive's vertices carry a bone label through nearest source-part center.
# Parts were joined; use world-space vertex proximity to each bone's bind center for robust rigid weighting.
centers={bn.name:Vector(bn.head_local) for bn in arm.data.bones}
for v in mesh.data.vertices:
 co=mesh.matrix_world @ v.co
 nearest=min(centers,key=lambda n:(co-centers[n]).length_squared)
 mesh.vertex_groups[nearest].add([v.index],1.0,'REPLACE')
mod=mesh.modifiers.new("Ryuo Armature","ARMATURE"); mod.object=arm
mesh.parent=arm
# Make a simple emissive energy ring on the right bracer.
bpy.ops.mesh.primitive_torus_add(major_radius=.12, minor_radius=.018, major_segments=20, minor_segments=6, location=(.54,.05,1.22))
ring=bpy.context.object; ring.name="Bracer Energy Ring"; ring.data.materials.append(cyan); ring.parent=arm
ring.parent_type='BONE'; ring.parent_bone="forearm.L"

# Animation helpers: keyframe bone rotations in Euler XYZ.
def action(name, frames, pose_fn, cyclic=False):
 bpy.context.view_layer.objects.active=arm
 bpy.ops.object.mode_set(mode="POSE")
 for pb in arm.pose.bones: pb.rotation_mode='XYZ'
 for frame in frames:
  bpy.context.scene.frame_set(frame)
  pose_fn(frame)
  for pb in arm.pose.bones:
   if pb.name not in ("root",): 
    pb.keyframe_insert(data_path="rotation_euler", frame=frame, group=pb.name)
 bpy.ops.object.mode_set(mode="OBJECT")
 act=arm.animation_data.action
 act.name=name
 act.use_cyclic=cyclic
 return act
def reset_pose(frame):
 for pb in arm.pose.bones: pb.rotation_euler=(0,0,0)
def idle_pose(frame):
 reset_pose(frame); v=math.sin(frame*math.pi/15)*.025
 arm.pose.bones["spine"].rotation_euler[0]=v
 arm.pose.bones["head"].rotation_euler[2]=v*.5
def walk_pose(frame):
 reset_pose(frame); a=math.sin(frame*math.pi/10)*.48
 arm.pose.bones["thigh.L"].rotation_euler[0]=a; arm.pose.bones["thigh.R"].rotation_euler[0]=-a
 arm.pose.bones["upper_arm.L"].rotation_euler[0]=-a*.65; arm.pose.bones["upper_arm.R"].rotation_euler[0]=a*.65
def punch_pose(frame):
 reset_pose(frame)
 k=max(0,math.sin((frame/12)*math.pi))
 arm.pose.bones["spine"].rotation_euler[2]=-.18*k
 arm.pose.bones["upper_arm.L"].rotation_euler[0]=-1.2*k
 arm.pose.bones["forearm.L"].rotation_euler[0]=-.6*k
def kick_pose(frame):
 reset_pose(frame); k=max(0,math.sin((frame/12)*math.pi))
 arm.pose.bones["thigh.L"].rotation_euler[0]=-1.15*k
 arm.pose.bones["spine"].rotation_euler[0]=.18*k
def jump_pose(frame):
 reset_pose(frame); k=math.sin((frame/16)*math.pi)
 arm.pose.bones["thigh.L"].rotation_euler[0]=-.55*k; arm.pose.bones["thigh.R"].rotation_euler[0]=-.55*k
 arm.pose.bones["upper_arm.L"].rotation_euler[0]=-1.1*k; arm.pose.bones["upper_arm.R"].rotation_euler[0]=-1.1*k
actions=[]
for name,frames,fn,cyclic in [
 ("Idle",[1,16,31],idle_pose,True),("Walk",[1,10,20],walk_pose,True),
 ("Punch",[1,6,12],punch_pose,False),("Kick",[1,6,12],kick_pose,False),
 ("Jump",[1,8,16],jump_pose,False),("Hit",[1,5,10],punch_pose,False),
 ("Special",[1,8,16],jump_pose,False),("Guard",[1,10,20],idle_pose,True)]:
 actions.append(action(name,frames,fn,cyclic))
# Pack scene to export multiple animation actions as NLA strips.
arm.animation_data.action=None
for act in actions:
 track=arm.animation_data.nla_tracks.new(); track.name=act.name
 strip=track.strips.new(act.name,1,act); strip.name=act.name; strip.blend_type='REPLACE'
# Set a clean T-pose bind and export.
bpy.context.scene.frame_set(1)
bpy.ops.object.select_all(action="DESELECT"); arm.select_set(True); mesh.select_set(True); ring.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=True, export_animations=True, export_nla_strips=True, export_skins=True, export_materials="EXPORT", export_apply=True)
print("Exported Ryuo GLB:", OUT)
