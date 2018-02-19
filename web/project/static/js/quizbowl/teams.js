
//enable dragging for 
var drake = dragula({
  isContainer: function (el) {
    return el.classList.contains('roster-pen');
  }
});
drake.containers.push(document.getElementById('player-pen'));

//dropping a player tile to a team assigns that player to that team
//dropping a player from a team back to the pen removes the team name
drake.on('drop', function(el, target, source, sibling) {
	if ( (el.classList.contains('player-tile')) && (target.classList.contains('roster-pen'))) {
		//to what team was this person dropped?
		assignedTeamId = target.parentNode.id
		playerId = el.id
		playerData = JSON.parse(sessionStorage.getItem(playerId))
		//console.log(JSON.parse(sessionStorage.getItem(playerId)))
		playerData['team'] = assignedTeamId
		sessionStorage.setItem(playerId, JSON.stringify(playerData))
	}
	if (el.classList.contains('roster-pen') && target.classList.contains('player-tile')) {
		playerId = target.id
		playerData = sessionStorage[playerId]
		playerData['team'] = null
		sessionStorage[playerId] = JSON.stringify(playerData);
	}
});


var teamPage = document.getElementById('team-pen');
teamPage.onclick = function(e) {
	if (e.target.id !== 'team-pen') {
		return false
	}
	for (i=0; i<3; i++){
		var teamId = 'team'+ i
		if (!sessionStorage[teamId]) {
			var teamName = prompt("Enter a team name!");
			if (teamName == null || teamName == "") {
    			return false
			} else {
			createTeam(teamId, teamName)
			return true
			}
		}
	}
};


function createTeam(teamId, teamName) {
	isDuplicate = isDuplicateName(teamName, teamId)
	while (isDuplicate) {
		teamName = prompt('team name already taken! try another')
		isDuplicate = isDuplicateName(teamName, teamId)
	}
	sessionData = createSessionData(teamId, teamName)
	createTeamTile(teamId, teamName)
	if(teamId=='team0') {
		updateFue()
	}
}


function createSessionData(teamId, teamName) {
	var teamPayload = {
		teamName: teamName,
		teamScore: 0
	}
	sessionStorage.setItem(teamId, JSON.stringify(teamPayload));
}


function isDuplicateName(proposalTeamName, proposalTeamId) {
	if (proposalTeamId=='team0') {
		return false
	}
	for (i=0;i<3;i++){
		teamId = 'team'+ i
		if (sessionStorage[teamId]) {
			var teamData = JSON.parse(sessionStorage[teamId]);
			if (teamData.teamName === proposalTeamName) {
				return true
			}
		}
	}
	return false
};


function createTeamTile(teamId) {
	var teamTile = document.createElement('div');
	var teamData = JSON.parse(sessionStorage[teamId]);
	teamTile.id = teamId;
	teamTile.className = 'col-md-4 team-tile';
	headerDiv = createTeamTileHeader(teamData);
	teamTile.appendChild(headerDiv);
	rosterDiv = createTeamRosterPen()
	teamTile.appendChild(rosterDiv);
	document.getElementById('team-pen').appendChild(teamTile);
	
}

function createTeamTileHeader(teamData) {
	//create team time header container
	var headerDiv = document.createElement('div');
	headerDiv.className = 'row team-tile-header';
	// create div with team name
	var teamNameDiv = document.createElement('div');
	teamNameDiv.innerHTML = teamData['teamName'];
	teamNameDiv.className = 'col-md-8 team-name';
	// create div with score
	var teamScoreDiv = document.createElement('div');
	teamScoreDiv.innerHTML = teamData['teamScore']
	teamScoreDiv.className = 'col-md-4 team-score'
	//append children to parent (headerDiv)
	headerDiv.appendChild(teamNameDiv);
	headerDiv.appendChild(teamScoreDiv);
	return headerDiv
}

function createTeamRosterPen() {
	rosterDiv = document.createElement('div');
	rosterDiv.className = 'row roster-pen'
	return rosterDiv

}


function updateFue() {

	var playersExist = document.getElementsByClassName("player-tile").length>0;
	var teamsExist = document.getElementsByClassName("team-tile").length>0;
	fueMessages = document.getElementsByClassName('fue-text');
	
	
	for (i=0; i<fueMessages.length; i++) {
		if (fueMessages[i].parentElement.id=='player-pen') {
			if (playersExist) {
				fueMessages[i].parentNode.removeChild(fueMessages[i])
			}
		}
		else if (fueMessages[i].parentElement.id=='team-pen') {
			if (teamsExist) {
				fueMessages[i].parentNode.removeChild(fueMessages[i])
			}
		}
		else if (fueMessages[i].parentElement.id=='game-pen') {
			if (teamsExist && playersExist) {
				fueMessages[i].innerHTML = "click to start the game!"
			}
			else if (!teamsExist && playersExist) {
				fueMessages[i].innerHTML = "add a team to start the game!"

			}
			else if (teamsExist && !playersExist) {
				fueMessages[i].innerHTML = "add players to start the game!"
			}
		}
	}
};

