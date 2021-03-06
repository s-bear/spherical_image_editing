import sphere_transforms as st
import sphere_transforms2 as st2
import numpy as np

size = (10,20)

ysize,xsize = size

#this is the format that st2 likes:
pts_o2 = np.indices(size).reshape((2,-1))

ys,xs = pts_o2[0],pts_o2[1]

#this is the format that st likes:
pts_o1 = list(zip(xs,ys))

#comparison function counts the number of terms that have a difference > eps
def compare(pts1,pts2,eps=0.00001,rev=False):
	if rev: #need to reorder x,y to y,x
		p1 = np.vstack(tuple(reversed(tuple(zip(*pts1)))))
	else:
		p1 = np.vstack(tuple(zip(*pts1)))
	return np.sum(np.abs(p1-pts2) > eps)

print('no transforms: {} different terms'.format(compare(pts_o1,pts_o2,rev=True)))

#go through a sequence of transforms and see if the results are the same
pts_oa1 = [st.angles_from_pixel_coords(pt,xsize) for pt in pts_o1]
pts_oa2 = st2.angles_from_pixel_coords(pts_o2,size)
print('angles_from_pixel_coords: {} different terms'.format(compare(pts_oa1,pts_oa2)))

pts_os1 = [st.sphere_from_angles(pt_a) for pt_a in pts_oa1]
pts_os2 = st2.sphere_from_angles(pts_oa2)
print('sphere_from_angles: {} different terms'.format(compare(pts_os1,pts_os2)))

pts_oc1 = [st.CP1_from_sphere(pt_s) for pt_s in pts_os1]
pts_oc2 = st2.CP1_from_sphere(pts_os2)
print('CP1_from_sphere: {} different terms'.format(compare(pts_oc1,pts_oc2)))

pts_is1 = [st.sphere_from_CP1(pt_c) for pt_c in pts_oc1]
pts_is2 = st2.sphere_from_CP1(pts_oc2)
print('sphere_from_CP1: {} different terms'.format(compare(pts_is1,pts_is2)))

pts_ia1 = [st.angles_from_sphere(pt_s) for pt_s in pts_is1]
pts_ia2 = st2.angles_from_sphere(pts_is2)
print('angles_from_sphere: {} different terms'.format(compare(pts_ia1,pts_ia2)))

pts_i1 = [st.pixel_coords_from_angles(pt_a,xsize) for pt_a in pts_ia1]
pts_i2 = st2.pixel_coords_from_angles(pts_ia2,size)
print('pixel_coords_from_angles: {} different terms'.format(compare(pts_i1,pts_i2,rev=True)))
