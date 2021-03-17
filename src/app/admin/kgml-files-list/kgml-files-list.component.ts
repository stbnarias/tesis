import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import { KgmlFilesService } from './kgml-files.service';
import { MatTableDataSource, MatSort, MatPaginator } from '@angular/material';
import {Location} from "@angular/common";

@Component({
  selector: 'app-kgml-files-list',
  templateUrl: './kgml-files-list.component.html',
  styleUrls: ['./kgml-files-list.component.css'],
  providers: [KgmlFilesService]
})
export class KgmlFilesListComponent implements OnInit {

  @ViewChild('fileInput') el:ElementRef;
  constructor(private service: KgmlFilesService, private location: Location) { }

  uploadedFile: any = null;
  file: any;
  files: any = [];
  filesData: MatTableDataSource<any>;
  displayedColumns: string[] = ['File Name', 'Created At', 'Actions'];
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  searchKey: string;

  ngOnInit() {
    this.service.getAllPathways().subscribe(files => {
      this.files = files;
      this.filesData = new MatTableDataSource<any>(files as
      {_id: string, name: string, file: BinaryType, graph: Object, image: BinaryType, createdAt: Date, updatedAt: Date, __v: number}[]);
      this.filesData.sort = this.sort;
      this.filesData.paginator = this.paginator;
    });
  }
  fileUpload() {
    console.log(this.el);
    // Access the uploaded file through the ElementRef
    this.uploadedFile = this.el.nativeElement.files[0];
    console.log(this.uploadedFile);
    console.log(this.service.uploadKGMLFileToDB(this.location.prepareExternalUrl("/api/upload"), this.uploadedFile));
  }

  postcargarxml(){
    this.service.uploadKGMLFileToDB(this.location.prepareExternalUrl("/api/upload"),this.file).subscribe(
      (data:any) => {
        console.log(data);
      }
    )
  }




}
