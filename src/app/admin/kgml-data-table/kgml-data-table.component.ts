import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatSort } from '@angular/material';
import { KgmlDataTableDataSource } from './kgml-data-table-datasource';

@Component({
  selector: 'app-kgml-data-table',
  templateUrl: './kgml-data-table.component.html',
  styleUrls: ['./kgml-data-table.component.css']
})
export class KgmlDataTableComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  dataSource: KgmlDataTableDataSource;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['id', 'name', 'amount'];

  ngOnInit() {
    this.dataSource = new KgmlDataTableDataSource(this.paginator, this.sort);
  }
}
