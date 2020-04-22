import { Component, OnInit, ElementRef, ViewChild, TemplateRef} from '@angular/core';
import { NgForm } from '@angular/forms';
import { DashboardService } from '../../services/dashboard.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Player, Players, Inputs } from '../../models/dashhboard';
import { ToastrService } from 'ngx-toastr';
import { NgxSpinnerService } from 'ngx-spinner';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Template } from '@angular/compiler/src/render3/r3_ast';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  players: Array<Object> = [];
  results: Array<Object> = [];
  userTeam: Array<Object> = [];
  teams: Array<Object> = [];
  homeActive: boolean = true;
  resultsActive: boolean = false;
  myDraftActive: boolean = false;
  draftSheetActive: boolean = false;
  infoActive: boolean = false;
  @ViewChild("middleA") middleA: ElementRef;
  @ViewChild("middleB") middleB: ElementRef;
  @ViewChild("middleK") middleK: ElementRef;
  @ViewChild("draftPlayer", {read: TemplateRef}) draftPlayer;
  inputModel: Inputs = new Inputs();
  inputsSet: boolean = false;
  draftType: String = "mock";
  scoringFormat: String = "h2h";
  draftFormat: String = "snake";
  modalRef: BsModalRef;
  optimumPick: any;
  isManuallySelecting: boolean = false;
  aboutToDraft: boolean = false;
  curPick: number = 1;
  showTeams: boolean = false;


  constructor(
    private dashboardService: DashboardService,
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private modalService: BsModalService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    console.log("Loading page...");
    this.dashboardService.getPlayers().then(res => {
      for (let i = 0; i < res.length; ++i) {
        let player = {};
        player["index"] = i;
        player["player"] = res[i].PLAYER;
        player["pos"] = res[i].POS;
        player["age"] = res[i].AGE;
        player["team"] = res[i].TEAM;
        player["fg%"] = res[i]["FG%"];
        player["ft%"] = res[i]["FT%"];
        player["3P"] = res[i]["3P"];
        player["pts"] = res[i].PTS;
        player["trb"] = res[i].TRB;
        player["ast"] = res[i].AST;
        player["stl"] = res[i].STL;
        player["tov"] = res[i].TOV;
        player["drafted"] = res[i].DRAFTED;
        this.players.push(player);
      }
      console.log(this.players);
    });
  }

  getInput(inputForm: NgForm) {
    if (inputForm.invalid) {
      console.log("INVALID");
      return;
    }
    let data = {
      league_name: this.inputModel.leagueName, 
      owner_name: this.inputModel.owner,
      team_name: this.inputModel.teamName,
      draft_type: this.draftType,
      scoring_format: this.scoringFormat,
      cats: this.inputModel.categories,
      draft_format: this.draftFormat,
      league_size: this.inputModel.leagueSize,
      draft_pos: this.inputModel.draftPos,
      team_size: this.inputModel.teamSize,
      to_punt: this.inputModel.punt
    };
    this.dashboardService.getInput(data).then(res => {
      console.log(res);
      this.inputsSet = true;
      this.setActive('draftsheet');
      console.log(this.inputsSet);
    });
  }

  simulatePick() {
    this.spinner.show();
    this.dashboardService.simulatePick().then(res => {
      console.log(res);
      this.spinner.hide();
      if (res.user) {
        //ask user if they want to draft player
        this.optimumPick = this.players[res.index];
        this.openModal(this.draftPlayer);
      } else {
        this.curPick += 1;
        this.players[res.index]["drafted"] = 1;
        this.results.push(this.players[res.index]);
        this.toastr.info("Opponent drafted " + this.players[res.index]["player"] + ".");
        if (this.curPick === (this.inputModel.leagueSize * this.inputModel.teamSize)) {
          this.setActive('results');
        }
      }
    });
  }

  pickPlayer() {
    this.modalRef.hide();
    let data = {
      index: this.optimumPick["index"]
    }
    this.dashboardService.pickPlayer(data).then(res => {
      console.log(res);
      this.curPick += 1;
      this.toastr.success("You drafted " + this.optimumPick["player"] + ".");
      this.players[this.optimumPick["index"]]["drafted"] = 1;
      this.results.push(this.players[this.optimumPick["index"]]);
      this.userTeam.push(this.players[this.optimumPick["index"]]);
      if (this.curPick === (this.inputModel.leagueSize * this.inputModel.teamSize)) {
        this.setActive('results');
      } else if (this.draftType === 'live' && res.user) {
        this.simulatePick();
      }
    });
  }

  manuallyPickPlayer(player) {
    let data = {
      index: player.index
    }
    this.dashboardService.pickPlayer(data).then(res => {
      console.log(res);
      this.curPick += 1;
      this.isManuallySelecting = false;
      this.toastr.success("You drafted " + this.players[player.index]["player"] + ".");
      this.players[player.index]["drafted"] = 1;
      this.results.push(player);
      this.userTeam.push(player);
      if (this.curPick === (this.inputModel.leagueSize * this.inputModel.teamSize)) {
        this.setActive('results');
      } else if (this.draftType === 'live' && res.user) {
        this.simulatePick();
      }
    });
  }

  removePlayer(player) {
    let data = {
      index: player.index
    }
    this.dashboardService.pickPlayer(data).then(res => {
      console.log(res);
      this.curPick += 1;
      this.toastr.info("Opponent drafted " + this.players[player.index]["player"] + ".");
      this.players[player.index]["drafted"] = 1;
      this.results.push(player);
      if (this.curPick === (this.inputModel.leagueSize * this.inputModel.teamSize)) {
        this.setActive('results');
      } else if (res.user) {
        this.simulatePick();
      }
    });
  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template);
  }

  getActive(value: string) {
    if (value === 'mydraft') {
      return this.myDraftActive ? 'navbar-active' : '';
    } else if (value === 'draftsheet') {
      return this.draftSheetActive ? 'navbar-active' : '';
    } else if (value === 'results') {
      return this.resultsActive ? 'navbar-active' : '';
    }
  }

  setActive(value: string) {
    if (value === 'mydraft') {
      this.myDraftActive = true;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.homeActive = false;
      this.infoActive = false;
    } else if (value === 'draftsheet') {
      this.draftSheetActive = true;
      this.myDraftActive = false;
      this.resultsActive = false;
      this.homeActive = false;
      this.infoActive = false;
      if (this.inputsSet) {
        if (this.inputModel.draftPos === 1 && this.draftType === 'live' && this.curPick === 1) {
          this.simulatePick();
        }
      }
    } else if (value === 'results') {
      this.teams = [];
      this.resultsActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.homeActive = false;
      this.infoActive = false;
      this.dashboardService.getTeams().then(res => {
        console.log(res);
        for(value in res) {
          this.teams.push(res[value]);
        }
        console.log(this.teams);
      });
    } else if (value === 'home') {
      this.homeActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.infoActive = false;
    } else if(value === 'info') {
      this.infoActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.homeActive = false;
    }
  }




  mouseoverAlexis(){
    this.middleA.nativeElement.style.opacity = "1";
  }

  mouseoutAlexis(){
    this.middleA.nativeElement.style.opacity = "0";
  }


  mouseoverBrennan(){
    this.middleB.nativeElement.style.opacity = "1";
  }

  mouseoutBrennan(){
    this.middleB.nativeElement.style.opacity = "0";
  }


  mouseoverKeara(){
    this.middleK.nativeElement.style.opacity = "1";
  }

  mouseoutKeara(){
    this.middleK.nativeElement.style.opacity = "0";
  }

  getFloor(value) {
    return Math.floor(value);
  }

  toggleTeams() {
    this.showTeams = !this.showTeams;
  }

}
