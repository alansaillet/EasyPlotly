# APP library

import plotly.graph_objs as go
import numpy as np

import os



colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'  # blue-teal
]

def Colors(i):
    colors = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf'  # blue-teal
    ]
    return colors[i%len(colors)]

def Init3DPlot(fig=None):
    if fig == None:
        fig = go.Figure()
        style = dict(
            backgroundcolor="rgba(0,0,0,0.1)",
            gridcolor="rgba(0,0,0,0.1)",
            showbackground=False,
            zerolinecolor="rgba(0,0,0,0.1)")
        fig.update_layout(scene=dict(xaxis=style, yaxis=style, zaxis=style))
        fig.update_layout(scene_aspectmode='manual',
                          scene_aspectratio=dict(x=1, y=1, z=1))
        fig.update_layout(scene_aspectmode='data',)
    return fig

def PlotTriangle3D(P0, P1, P2, fig=None, show=False, facecolor =None):
    fig = Init3DPlot(fig=fig)
    data = []

    facecolorlist = (facecolor,None) #Just because the facecolor requires a list, even if we plot only one face...


    Points = np.array([P0, P1, P2])
    if facecolor == None:
        trace = go.Mesh3d(x=Points[:, 0], y=Points[:, 1], z=Points[:, 2])
    else:
        trace = go.Mesh3d(x=Points[:, 0], y=Points[:, 1], z=Points[:, 2],facecolor = facecolorlist)
    data.append(trace)

    for trace in data:
        fig.add_trace(trace)
    if show:
        fig.show()

    return fig

def coloscale_i(i):
    return [(0, colors[i]), (1, colors[i])]

def PlotArrow(P0,P1=None, V=None,show=False, showArrow=True, showMarkers=True, fig=None, colorNum=0):
    fig = Init3DPlot(fig=fig)

    if P1 is None and V is None:
        Points = np.transpose([P0])
    else:
        if P1 is not None:
            V = P1 - P0
        elif V is not None:
            P1 = P0 + V
        """V /= np.linalg.norm(V[:3])"""
        Points = np.transpose([P0, P1])

    j = colorNum

    line = dict(color=colors[j])
    trace = go.Scatter3d(x=Points[0, :], y=Points[1, :], z=Points[2, :], mode='lines',line=line, showlegend=False)
    fig.add_trace(trace)

    if showMarkers:
        marker = dict(size=2, opacity=0.4, color=colors[j])
        trace = go.Scatter3d(x=Points[0, :], y=Points[1, :], z=Points[2, :], mode='markers', marker=marker, showlegend=False)
        fig.add_trace(trace)

    if showArrow and V is not None:
        trace = go.Cone(x=[P1[0]], y=[P1[1]], z=[P1[2]], u=[V[0]], v=[V[1]], w=[V[2]], colorscale=coloscale_i(j))
        fig.add_trace(trace)

    if show:
        fig.show()
    return fig

def PlotGridElement3D(X,Y,Z,i=0,j=0, show=False, fig=None,facecolor="red",colorNum=1):
    fig = Init3DPlot(fig=fig)
    data = []

    i = int(i)
    j = int(j)
    point_1 = np.asarray([X,Y,Z])[:, j, i]
    point_2 = np.asarray([X,Y,Z])[:, j, i+1]
    point_3 = np.asarray([X,Y,Z])[:, j+1, i+1]
    point_4 = np.asarray([X,Y,Z])[:, j+1, i]

    points3D = np.asarray([point_1,point_2,point_3,point_4,point_1]).T

    line = dict(
        color="rgba(0,0,0,0)"
    )

    trace = go.Mesh3d(x=points3D[0,:], y=points3D[1,:], z=points3D[2,:])
    data.append(trace)

    for trace in data:
        fig.add_trace(trace)
    if show:
        fig.show()
    return fig

def plotPoint3D(P0,fig=None,colorNum=None,color="black",markersize=3):
    fig = Init3DPlot(fig=fig)

    if colorNum == None:
        marker = dict(
            size=markersize,
            opacity=1,
            color = color
        )
    else:
        marker = dict(
            size=markersize,
            opacity=1,
            color=colors[colorNum]
        )
    trace = go.Scatter3d(x=[P0[0]], y=[P0[1]],z=[P0[2]], mode='markers',marker=marker)
    fig.add_trace(trace)
    return fig

def make_orthographic(fig=None):
    fig = Init3DPlot(fig=fig)
    layout = dict(scene=dict(camera=dict(projection=dict(type="orthographic"))))
    fig.update_layout(layout)
    return fig

def saveFigToFile(fig, name, visualXpixelsSize, actualXpixelsSize, filepath="images"):

    boundsExist = fig.layout.xaxis.range != None and fig.layout.yaxis.range != None
    if boundsExist:
        lx = np.diff(fig.layout.xaxis.range)[0]
        ly = np.diff(fig.layout.yaxis.range)[0]
        aspect_ratio = lx / ly
    else:
        aspect_ratio = 1
    visualypixelsSize = int(visualXpixelsSize / aspect_ratio)
    scaling = actualXpixelsSize / visualypixelsSize

    if not os.path.exists(filepath):
        os.mkdir(filepath)

    img_bytes = fig.to_image(format="png", width=visualXpixelsSize, height=visualypixelsSize, scale=scaling)
    outF = open(filepath+"/"+name, "wb")
    outF.write(img_bytes)
    outF.close()

if __name__ == '__main__':
    P0 = [11, 1, 6, 1]
    P1 = [16, 10, 7, 1]
    P2 = [18, 4, 8, 1]
    PlotTriangle3D(P0, P1, P2, show=True)