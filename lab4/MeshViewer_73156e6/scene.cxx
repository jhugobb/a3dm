// ---------------------------------------------------------------------
//     MeshViewer
// Copyright (c) 2019, The ViRVIG resesarch group, U.P.C.
// https://www.virvig.eu
//
// This file is part of MeshViewer
// MeshViewer is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
// ---------------------------------------------------------------------
#include "scene.h"
#include <iostream>
#include <OpenMesh/Core/Utils/vector_cast.hh>

Scene::Scene() {
  threshold = 0;  
}

Scene::~Scene() {}

float Scene::getMinVal() {
  return min;
}

float Scene::getMaxVal() {
  return max;
}

void Scene::setThreshold(float t) {
  threshold = t;
}

float Scene::getThreshold() {
  return threshold;
}

bool Scene::load(const char* name) {
  MyMesh m;
  ColorInfo ci = NONE;
  // request desired props:
  m.request_face_normals();
  m.request_face_colors();
  m.request_vertex_normals();
  m.request_vertex_colors();
  OpenMesh::IO::Options opt(OpenMesh::IO::Options::FaceColor |
			    OpenMesh::IO::Options::VertexColor |
			    OpenMesh::IO::Options::FaceNormal |
			    OpenMesh::IO::Options::VertexNormal);
  if (not OpenMesh::IO::read_mesh(m, name, opt)) {
    std::cerr << "Error loading mesh from file " << name  << std::endl;
    return false;
  }
  if (opt.check(OpenMesh::IO::Options::FaceNormal))  {
    std::cout << "File "<<name<<" provides face normals\n";
  } else {
    std::cout << "File "<<name<<" MISSING face normals\n";
  }
  // check for possible color information
  if (opt.check(OpenMesh::IO::Options::VertexColor))  {
    std::cout << "File "<<name<<" provides vertex colors\n";
    ci = VERTEX_COLORS;
  } else {
    std::cout << "File "<<name<<" MISSING vertex colors\n";
  }    
  if (opt.check(OpenMesh::IO::Options::FaceColor)) {
    std::cout << "File "<<name<<" provides face colors\n";
    ci = FACE_COLORS;
  } else {
    std::cout << "File "<<name<<" MISSING face colors\n";
  }
  if (not opt.check(OpenMesh::IO::Options::FaceNormal)) {
    m.update_face_normals();
  }
  if (not opt.check(OpenMesh::IO::Options::VertexNormal)) {
    m.update_vertex_normals();
  }
  _meshes.push_back(std::pair<MyMesh, ColorInfo>(m, ci));
  return true;
}

void Scene::addCube() {
  MyMesh m;
  // Add vertices
  MyMesh::VertexHandle vhandle[8];
  vhandle[0] = m.add_vertex(MyMesh::Point(-1, -1,  1));
  vhandle[1] = m.add_vertex(MyMesh::Point( 1, -1,  1));
  vhandle[2] = m.add_vertex(MyMesh::Point( 1,  1,  1));
  vhandle[3] = m.add_vertex(MyMesh::Point(-1,  1,  1));
  vhandle[4] = m.add_vertex(MyMesh::Point(-1, -1, -1));
  vhandle[5] = m.add_vertex(MyMesh::Point( 1, -1, -1));
  vhandle[6] = m.add_vertex(MyMesh::Point( 1,  1, -1));
  vhandle[7] = m.add_vertex(MyMesh::Point(-1,  1, -1));
  // Add (triangular) faces:
  std::vector<MyMesh::VertexHandle>  face_vhandles;
  MyMesh::FaceHandle face;
  face_vhandles.clear(); //front
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)   
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 0., 1.));
  face_vhandles.clear(); 
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1) 
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 0., 1.));
  face_vhandles.clear(); // back
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 0., 1.));
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 0., 1.));
  face_vhandles.clear(); // top
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1)
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 1., 0.));
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 1., 0.));
  face_vhandles.clear(); // bottom
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 1., 0.));
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(0., 1., 0.));
  face_vhandles.clear(); // left
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1)
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(1., 0., 0.));
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(1., 0., 0.));
  face_vhandles.clear(); // right
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(1., 0., 0.));
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face = m.add_face(face_vhandles);
  m.set_color(face, MyMesh::Color(1., 0., 0.));
  m.update_normals();
  _meshes.push_back(std::pair<MyMesh,ColorInfo>(std::move(m), FACE_COLORS));
}
void Scene::addCubeVertexcolors() {
  MyMesh m;
  // Add vertices
  MyMesh::VertexHandle vh, vhandle[8];
  vh = m.add_vertex(MyMesh::Point(-1, -1,  1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[0] = vh;
  vh = m.add_vertex(MyMesh::Point( 1, -1,  1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[1] = vh;
  vh = m.add_vertex(MyMesh::Point( 1,  1,  1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[2] = vh;
  vh = m.add_vertex(MyMesh::Point(-1,  1,  1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[3] = vh;
  vh = m.add_vertex(MyMesh::Point(-1, -1, -1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[4] = vh;
  vh = m.add_vertex(MyMesh::Point( 1, -1, -1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[5] = vh;
  vh = m.add_vertex(MyMesh::Point( 1,  1, -1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[6] = vh;
  vh = m.add_vertex(MyMesh::Point(-1,  1, -1));
  m.set_normal(vh,OpenMesh::vector_cast<OpenMesh::Vec3f>(m.point(vh)));
  m.set_color(vh, (m.normal(vh)+OpenMesh::Vec3f(1, 1, 1))*.5);
  vhandle[7] = vh;
  
  // Add (triangular) faces:
  std::vector<MyMesh::VertexHandle>  face_vhandles;
  MyMesh::FaceHandle face;
  face_vhandles.clear(); //front
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)   
  face = m.add_face(face_vhandles);
  face_vhandles.clear(); 
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1) 
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear(); // back
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear(); // top
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1)
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear(); // bottom
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear(); // left
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[3]); // (-1,  1,  1)
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
  face_vhandles.push_back(vhandle[7]); // (-1,  1, -1)
  face_vhandles.push_back(vhandle[4]); // (-1, -1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear(); // right
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[1]); // ( 1, -1,  1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face = m.add_face(face_vhandles);
  face_vhandles.clear();
  face_vhandles.push_back(vhandle[2]); // ( 1,  1,  1)
  face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
  face_vhandles.push_back(vhandle[6]); // ( 1,  1, -1)
  face = m.add_face(face_vhandles);
  _meshes.push_back(std::pair<MyMesh,ColorInfo>(std::move(m), VERTEX_COLORS));
}

void Scene::loadScalarField(QString filename) {
  min = std::numeric_limits<float>::max();
  max = std::numeric_limits<float>::min();
  scalar_field = std::vector<float>();
  int voxelization_size; 
  std::ifstream file(filename.toStdString());
  std::string line;
  unsigned int v = 0;
  while (std::getline(file, line)) {
    QString l = QString(line.c_str());
    if (v==0){
      voxelization_size = l.toInt();
      v++;
    } else {
      float f = l.toFloat();
      scalar_field.push_back(f);
      if (f < min) min = f;
      if (f > max) max = f;
    }
  }
  float value;
  float half = 1;
  MyMesh m;
  for (int i=0; i<voxelization_size; i++) {
    for (int j=0; j<voxelization_size; j++) {
      for (int k=0; k<voxelization_size; k++) {
        value = scalar_field[i*voxelization_size*voxelization_size + j*voxelization_size + k];
        // Add vertices
        if (value < threshold) {
          MyMesh::VertexHandle vhandle[6];
          vhandle[0] = m.add_vertex(MyMesh::Point(i, j, k) + MyMesh::Point( half,  0,  0));
          vhandle[1] = m.add_vertex(MyMesh::Point(i, j, k) + MyMesh::Point(-half,  0,  0));
          vhandle[2] = m.add_vertex(MyMesh::Point(i, j, k) + MyMesh::Point( 0,  half,  0));
          vhandle[3] = m.add_vertex(MyMesh::Point(i, j, k) + MyMesh::Point( 0, -half,  0));
          vhandle[4] = m.add_vertex(MyMesh::Point(i, j, k) + MyMesh::Point( 0,  0,  half));
          vhandle[5] = m.add_vertex(MyMesh::Point(i, j, k) + MyMesh::Point( 0,  0, -half));

          // Add (triangular) faces:
          std::vector<MyMesh::VertexHandle>  face_vhandles;
          MyMesh::FaceHandle face;
          face_vhandles.clear(); //front
          face_vhandles.push_back(vhandle[0]); // (-1, -1,  1)
          face_vhandles.push_back(vhandle[2]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[4]); // ( 1,  1,  1)   
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(0., 0., 1.));
          face_vhandles.clear(); 
          face_vhandles.push_back(vhandle[0]); // ( 1,  1,  1)
          face_vhandles.push_back(vhandle[4]); // (-1,  1,  1) 
          face_vhandles.push_back(vhandle[3]); // (-1, -1,  1)
          face = m.add_face(face_vhandles);
          face_vhandles.clear(); // bottom
          face_vhandles.push_back(vhandle[0]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[3]); // (-1, -1,  1)
          face_vhandles.push_back(vhandle[5]); // (-1, -1, -1)
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(0., 1., 0.));
          face_vhandles.clear();
          face_vhandles.push_back(vhandle[0]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[5]); // (-1, -1, -1)
          face_vhandles.push_back(vhandle[2]); // ( 1, -1, -1)
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(0., 1., 0.));
          face_vhandles.clear(); // right
          face_vhandles.push_back(vhandle[1]); // ( 1,  1,  1)
          face_vhandles.push_back(vhandle[4]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[2]); // ( 1, -1, -1)
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(1., 0., 0.));
          face_vhandles.clear(); // right
          face_vhandles.push_back(vhandle[1]); // ( 1,  1,  1)
          face_vhandles.push_back(vhandle[2]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[5]); // ( 1, -1, -1)
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(1., 0., 0.));
          face_vhandles.clear(); // right
          face_vhandles.push_back(vhandle[1]); // ( 1,  1,  1)
          face_vhandles.push_back(vhandle[5]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[3]); // ( 1, -1, -1)
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(1., 0., 0.));
          face_vhandles.clear(); // right
          face_vhandles.push_back(vhandle[1]); // ( 1,  1,  1)
          face_vhandles.push_back(vhandle[3]); // ( 1, -1,  1)
          face_vhandles.push_back(vhandle[4]); // ( 1, -1, -1)
          face = m.add_face(face_vhandles);
          m.set_color(face, MyMesh::Color(1., 0., 0.));
        }
      }
    }
  }
  m.update_normals();
  _meshes.push_back(std::pair<MyMesh,ColorInfo>(std::move(m), FACE_COLORS));
}

void Scene::loadMC(QString filename) {
  min = std::numeric_limits<float>::max();
  max = std::numeric_limits<float>::min();
  scalar_field = std::vector<float>();
  int voxelization_size; 
  std::ifstream file(filename.toStdString());
  std::string line;
  unsigned int v = 0;
  while (std::getline(file, line)) {
    QString l = QString(line.c_str());
    if (v==0){
      voxelization_size = l.toInt();
      v++;
    } else {
      float f = l.toFloat();
      scalar_field.push_back(f);
      if (f < min) min = f;
      if (f > max) max = f;
    }
  }
  float value;
  MyMesh m;
  std::vector<QVector3D> verts;
  std::vector<int> b(voxelization_size*voxelization_size*voxelization_size,0);
  for (int i=0; i<voxelization_size; i++) {
    for (int j=0; j<voxelization_size; j++) {
      for (int k=0; k<voxelization_size; k++) {
        value = scalar_field[i*voxelization_size*voxelization_size + j*voxelization_size + k];
        // Add vertices
        if (value < threshold) {
          b.at(i*voxelization_size*voxelization_size + j*voxelization_size + k) = 1;
        } else b.at(i*voxelization_size*voxelization_size + j*voxelization_size + k) = 0;
      }
    }
  }

  for (int i=0; i<voxelization_size*voxelization_size*voxelization_size; i++) {
    int z = fmod(i,voxelization_size);              //z
    int y = (fmod(i, voxelization_size*voxelization_size) - z) / voxelization_size; //y
    int x = (i - y*voxelization_size - z) / (voxelization_size*voxelization_size); //x
    verts.push_back(QVector3D(x,y,z));
  }
  int cas;
  std::vector<std::vector<int>> top;
  for (int i=0; i<voxelization_size-1; i++) {
    for (int j=0; j<voxelization_size-1; j++) {
      for (int k=0; k<voxelization_size-1; k++) {
        int v1 = i*voxelization_size*voxelization_size + j*voxelization_size + k;
        int v2 = i*voxelization_size*voxelization_size + (j+1)*voxelization_size + k;
        int v3 = i*voxelization_size*voxelization_size + j*voxelization_size + k+1;
        int v4 = i*voxelization_size*voxelization_size + (j+1)*voxelization_size + k+1;
        int v5 = (i+1)*voxelization_size*voxelization_size + j*voxelization_size + k;
        int v6 = (i+1)*voxelization_size*voxelization_size + (j+1)*voxelization_size + k;
        int v7 = (i+1)*voxelization_size*voxelization_size + j*voxelization_size + k+1;
        int v8 = (i+1)*voxelization_size*voxelization_size + (j+1)*voxelization_size + k+1;

        cas = b[v1]*128 + b[v2]*64 + b[v3]*32 + b[v4]*16 + b[v5]*8 + b[v6]*4 + b[v7]*2 + b[v8];
        top = casos[cas];
        std::vector<MyMesh::VertexHandle> face_vhandles;
        QVector3D n;
        MyMesh::FaceHandle face;
        for (unsigned int q = 0; q < top.size(); q++){
          MyMesh::VertexHandle vhandle[3];

          for (unsigned int c = 0; c < top[q].size(); c++) {
            switch (top.at(q).at(c)) {
              case 0:
                n = linear_interpolation(verts[v1], 0, verts[v5], 4, 0);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 1:
                n = linear_interpolation(verts[v5], 4, verts[v6], 5, 1);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 2:
                n = linear_interpolation(verts[v6], 5, verts[v2], 1, 2);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 3:
                n = linear_interpolation(verts[v2], 1, verts[v1], 0, 3);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 4:
                n = linear_interpolation(verts[v3], 2, verts[v7], 6, 4);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 5:
                n = linear_interpolation(verts[v7], 6, verts[v8], 7, 5);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 6:
                n = linear_interpolation(verts[v8], 7, verts[v4], 3, 6);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 7:
                n = linear_interpolation(verts[v4], 3, verts[v3], 2, 7);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 8:
                n = linear_interpolation(verts[v7], 6, verts[v5], 4, 8);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 9:
                n = linear_interpolation(verts[v8], 7, verts[v6], 5, 9);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 10:
                n = linear_interpolation(verts[v3], 2, verts[v1], 0, 10);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
              case 11:
                n = linear_interpolation(verts[v4], 3, verts[v2], 1, 11);
                vhandle[c] = m.add_vertex(MyMesh::Point(n.x(),n.y(),n.z()));
                face_vhandles.push_back(vhandle[c]);
                break;
            }
          }
          if (top[q].size() != 0) {
            face = m.add_face(face_vhandles);
            m.set_color(face, MyMesh::Color(1., 0., 0.));
            face_vhandles.clear();
          }
        }
      }
    }
  }
  m.update_normals();
  _meshes.push_back(std::pair<MyMesh,ColorInfo>(std::move(m), NONE));
}

QVector3D Scene::linear_interpolation(QVector3D a, int va, QVector3D b, int vb, int v) {
  QVector3D res = QVector3D(0,0,0);
  float f = (float(vb-v)/float(vb-va));
  float f2 = (float(v-va)/float(vb-va));
  res.setX(a.x()*f+b.x()*f2);
  res.setY(a.y()*f+b.y()*f2);
  res.setZ(a.z()*f+b.z()*f2);
  return res;
}