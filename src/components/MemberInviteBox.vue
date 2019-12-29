<template>
  <div>
    <h1> Invite an user </h1>
    <input v-model="invitedEmail" type="text" placeholder="Enter their email..." />
    <button @click="inviteUser"> Invite! </button>
  </div>
</template>

<script>
import { db } from "../firebase/init";

export default {
  name: "MemberInviteBox",
  data: function() {
    return {
      invitedEmail: ""
    };
  },
  methods: {
    inviteUser: function () {
      let invitedEmail = this.invitedEmail;
      if (invitedEmail == "") {
        // throwing error
        alert("You should enter an email");
      } else {
        // TODO: replace with a firebase function. params (invitedUser)
        // - Verify that user has a team
        // - Create a Invitation record with Inviter, Invitee and Inviter's TeamID
        // - Add the Invitation to team record
        // RETURN: results of operation

        // ======================================
        let userID = this.$store.getters.getUser.uid;
        console.log(userID);
        let userRef = db.collection("users").doc("MT0LhHggQaeo62pcRbnLtrIMdFI3");
        let getUser = userRef.get().then(userDoc => {
          if (!userDoc.exists) {
            console.log(`Cannot find user id ${userID}`);
          } else {
            let teamID = userDoc.data().teamID;
            if (teamID == "") {
              console.log("User is not in a team!!");
            } else {
              let teamRef = db.collection('teams').doc(teamID)
              let getTeam = teamRef.get()
                .then(teamDoc => {
                  if (!teamDoc.exists) {
                    console.log(`Cannot find team ID ${teamID}`);
                  } else {
                    let queryInvited = db.collection('users').where('email', '==', this.invitedEmail).get()
                      .then(results => {
                        if (results.empty) {
                          alert("Cannot find this email");
                          return
                        }

                        results.forEach(inviteeDoc => {
                          let teamInviteData = {
                            inviterID: userID,
                            inviteeID: inviteeDoc.data().uid,
                            teamID: teamID
                          };

                          let addInvitation = db
                            .collection("teamInvites")
                            .add(teamInviteData)
                            .then(ref => {
                              let inviteID = ref.id;
                              console.log(`Adding invite ID ${inviteID} to team ${teamID}`)
                              let teamInvites = teamDoc.data().teamInvites;
                              teamInvites.push(inviteID);
                              let updateInvitations = teamRef.update({
                                teamInvites: teamInvites
                              });
                            });
                        });
                      }); 
                  }
                });  
            }   
          }
        });
        // ====================================== END OF FIREBASE FUNCTION
      }
    }
  }

}
</script>