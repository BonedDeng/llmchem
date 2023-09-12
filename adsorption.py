import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.data import covalent_radii
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import os

def get_surf_by_Z(atoms, zRange):
    myPos = atoms.get_positions()
    return [
        i for i in range(len(atoms))\
        if min(zRange) < myPos[i][2] < max(zRange)
    ]
def get_surfAtom_byXY(atoms, xypos, scale=2):
    radiiAll = scale * np.array([
        covalent_radii[i] for i in atoms.get_atomic_numbers()])
    z_test = max(atoms.get_positions()[:, 2])+5
    surfIndex = []
    while len(surfIndex) == 0:
        testAtom = Atoms(['H'], [[xypos[0], xypos[1], z_test]])
        tmpAtoms = atoms.copy()
        tmpAtoms.extend(testAtom)
        dist_test = list(tmpAtoms.get_distances(-1, list(range(len(atoms)))) - radiiAll)
        for i in dist_test:
            if i < 0: surfIndex.append(dist_test.index(i))
        z_test -= 0.1
    return surfIndex
def get_extended_atoms(atoms):
    tmpAtoms = atoms.copy()
    tmpAtoms = atoms*[3,3,1]
    tmpAtoms.set_positions(tmpAtoms.get_positions()\
        -atoms.get_cell()[0]-atoms.get_cell()[1])
    return tmpAtoms
#
# def simplex():
    # pos_ext = surf_ext.get_positions()
    # tri = Delaunay(pos_ext[:, :2])
    # pos_nodes = pos_ext[tri.simplices]

    # hollow = np.array([t.sum(axis=0) / 3 for t in pos_nodes])

    # bridge = []
    # for i in pos_nodes:
    #     bridge.append((i[0] + i[1]) / 2)
    #     bridge.append((i[0] + i[2]) / 2)
    #     bridge.append((i[1] + i[2]) / 2)
    # bridge = np.array(bridge)
def get_surf_grid(atoms, mesh=100):
    cell = atoms.get_cell()
    grids = np.linspace(0, 1, mesh, endpoint=False)
    surfList = []
    for i,j in zip(grids, grids):
        surfList += get_surfAtom_byXY(atoms,\
            [cell[0][0]*i+cell[1][0]*j, cell[0][2]*i+cell[1][1]*j])
    return sorted(list(set(surfList)))
# def plot():
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.triplot(pos_ext[:,0], pos_ext[:,1], triangles=tri.simplices, color='grey',)
#     ax.plot(hollow[:,0],  hollow[:,1],  'ok', label='Hollow')
#     ax.plot(bridge[:,0],  bridge[:,1],  'or', label='Bridge')
#     ax.plot(pos_ext[:,0], pos_ext[:,1], 'ob', label='Atop')
#     plt.legend(loc='lower left')
#     plt.axis('scaled')
#
#     cell_param = surf.get_cell()
#     ax.set_xlim([cell_param[1][0],cell_param[0][0]])
#     ax.set_ylim([cell_param[0][1],cell_param[1][1]])
#
#     plt.savefig('ads.png',  bbox_inches = "tight", transparent=True)
#
#     write('surf.png', surf)
def plot(atop):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # ax.plot(hollow[:, 0], hollow[:, 1], 'ok', label='Hollow')
    ax.plot(atop[:, 0][-1], atop[:, 1][-1], 'or', label='Bridge')
    ax.plot(atop[:, 0][0:-1], atop[:, 1][0:-1], 'ob', label='Atop')
    plt.legend(loc='lower left')
    plt.axis('scaled')

    cell_param = surf.get_cell()
    ax.set_xlim([cell_param[1][0], cell_param[0][0]])
    ax.set_ylim([cell_param[0][1], cell_param[1][1]])

    plt.savefig('ads.png', bbox_inches="tight", transparent=True)

    write('surf.png', surf)
def tihuanyuanzi(surf):
    for i, atom in enumerate(surf):
        if atom.symbol == "F":
            surf[i].symbol = "Si"
        # print(atom.index)
def guanzi():
    #把二维材料卷成管子(x方向, 往上卷, 卷完管子周期方向沿z轴)
    from ase.io import read, write
    import sys
    import numpy as np
    a = read(sys.argv[1])
    a.center()
    R = a.cell[0, 0] / 2 / 3.1415926
    D_ang = 2 * np.pi / a.cell[0, 0]
    center_z = a.get_positions().mean(axis=0)[2]
    for i in a:
        Ri = R - (i.z - center_z)
        theta = i.x * D_ang
        i.x = Ri * np.cos(theta)
        i.z = Ri * np.sin(theta)
    a.set_cell([2 * R + 16, a.cell[1, 1], 2 * R + 16])
    a.center()
    write("a.vasp", a)
def jianchang():
    #健长分析
    from ase.io import read
    import numpy as np
    a = read("POSCAR")
    dist = []
    ind = []
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            ind.append([i, j])
            dist.append(a.get_distance(i, j))
    dist = np.array(dist)
    order = np.argsort(dist)
    ind = np.array(ind)
    ii = ind[order, 0]
    jj = ind[order, 1]
    d = np.sort(dist)
    print("atom_index1 atom_index2 distance")
    for i in range(10 if len(d) > 10 else len(d)):
        print("%d    %d    %.3f" % (ii[i], jj[i], d[i]))
def rdf(fname, nbins):
    from ase.geometry.analysis import Analysis
    from scipy.ndimage import gaussian_filter1d
    from ase.io import read
    traj = read("%s.dump" % fname, index="-20:")
    res = Analysis(traj).get_rdf(rmax=4, nbins=500, elements='Mo', return_dists=True)
    r = res[0][1]
    rdf = np.zeros(nbins)
    for i in res:
        rdf += i[0]
    rdf = gaussian_filter1d(rdf / len(res))  # smoothing
if __name__ == '__main__':
    folder_path = '/Users/user/Desktop/project/script/posecargenergate/xsd/si/'
    outpath = '/Users/user/Desktop/project/script/posecargenergate/xsd/h/sih/'
    for i in range(1,32):
        dirname = outpath + str(i)
        os.mkdir(dirname)
        file_name = str(i)+'/POSCAR'
        outfile_name = str(i)+"/POSCAR"
        file_path = os.path.join(folder_path, file_name)
        outfile_path = os.path.join(outpath, file_name)
        # print(file_path)
        surf = read(file_path)
        print(surf)

        if os.path.isfile(file_path):
            atop = surf.get_positions()
            adsorptsite = atop[-1]
            ads_coordH = np.array([[0, 0, 0]])
            # ads_coordCO = np.array([[0, 0, 0], [0, 0, 1.17]])
            # ads_coordCOOH = np.array([[0, 0, 0], [0, 1, 0.6], [0, -1, 0.6], [0, -1, 1.6]])
            surf.extend(Atoms('H', ads_coordH + adsorptsite + np.array([0, 0, 1.7])))
            # surf.extend(Atoms('CO', ads_coordCO + adsorptsite + np.array([0, 0, 1.9])))
        # tihuanyuanzi(surf)
            surf.wrap()
            write(outfile_path, surf)

    # atop = surf.get_positions()
    # plot(atop)
    # ads_coordCO = np.array([[0, 0, 0], [0, 0, 1.17]])  # CO bondlength
    # ads_coordCOOH = np.array([[0, 0, 0], [0, 1, 0.6], [0, -1, 0.6], [0, -1, 1.6]])  # COOH bondlength
    # # print(atop[-1])
    # adsorptsite = atop[-1]
    # # surf.extend(Atoms('CO', ads_coordCO + adsorptsite + np.array([0, 0, 1.9])))
    # # surf.extend(Atoms('COOH', ads_coordCOOH + adsorptsite + np.array([0, 0, 1.9])))
    # surf.wrap()
    # write('ads_surfCOOH.vasp', surf)
    # print(surf,atop)
